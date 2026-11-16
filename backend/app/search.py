from dataclasses import dataclass
from sqlalchemy import select
from app.database import SessionLocal
from app.embeddings import encode_passages
from app.models import Chunk, Document



@dataclass(frozen=True)
class SearchHit:
    chunk_id: int
    filename: str
    page_number: int | None
    content: str
    score: float

    
def dense_search(question: str, limit: int = 8) -> list[SearchHit]:
    vector = encode_passages([question])[0]
    distance = Chunk.embedding.cosine_distance(vector).label("distance")
    stmt = (
        select(Chunk, Document.filename, distance)
        .join(Document, Chunk.document_id == Document.id)
        .where(Chunk.embedding.is_not(None))
        .order_by(distance).limit(limit)
    )
    with SessionLocal() as session:
        rows = session.execute(stmt).all()
    return [SearchHit(c.id, filename, c.page_number, c.content,
                      1.0 - float(dist)) for c, filename, dist in rows]