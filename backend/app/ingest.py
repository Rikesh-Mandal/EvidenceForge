from __future__ import annotations
from hashlib import sha256
from pathlib import Path
from uuid import UUID
import pymupdf
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Chunk, Document


MAX_UPLOAD_BYTES = 5 * 1024 * 1024

def extract_pages(filename: str, data: bytes) -> list[tuple[int | None, str]]:
    suffix = Path(filename).suffix.lower()
    if not data or len(data) > MAX_UPLOAD_BYTES:
        raise ValueError("File is empty or exceeds the 5 Mb limit")
    if suffix == ".txt":
        return[(None, data.decode("utf-8-sig"))]
    if suffix == ".pdf":
        try:
            with pymupdf.open(stream=data, filetype="pdf") as doc:
                if doc.needs_pass:
                    raise ValueError("Password protected PDFs are unsupported")
                if len(doc) > 150:
                    raise ValueError("PDF has more than 150 pages")
                return[(i + 1, page.get_text("text"))
                       for i, page in enumerate(doc)]
        except (pymupdf.FileDataError, pymupdf.EmptyFileError) as exc:
            raise ValueError("Invalid PDF") from exc
    raise ValueError("Only .txt and text-based .pdf are supported")


def chunk_pages(pages: list[tuple[int | None, str]], size: int = 180, overlap: int = 30) -> list[dict]:
    if not 0 <= overlap < size:
        raise ValueError("Expected 0 <= overlap < size")
    chunks = []
    for page_number, text in pages:
        words = text.split()
        step = size - overlap
        for start in range (0, len(words), step):
            selection = words[start:start + size]
            if selection:
                chunks.append({"page_number": page_number,
                               "content": " ".join(selection)})
            if start + size >= len(words):
                break
    return chunks


def ingest_bytes(filename: str, data: bytes) -> tuple[UUID, int, bool]:
    pages = extract_pages(filename, data)
    pieces = chunk_pages(pages)
    if not pieces:
        raise ValueError("No extractable text")
    digest =sha256(data).hexdigest()
    with SessionLocal.begin() as session:
        old = session.scalar(select(Document).where(Document.sha256 == digest))
        if old is not None:
            return old.id, len(old.chunks), True
        document = Document(filename=Path(filename).name, sha256=digest)
        session.add(document)
        session.flush()
        for ordinal, piece in enumerate(pieces):
            session.add(Chunk(
                document_id=document.id, ordinal=ordinal,
                page_number=piece["page_number"], content=piece["content"],
            ))
        return document.id, len(pieces), False

