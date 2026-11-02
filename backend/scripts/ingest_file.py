import argparse
from pathlib import Path
from app.ingest import ingest_bytes
parser = argparse.ArgumentParser(description="Ingest a training document")
parser.add_argument("file", type=Path)
args = parser.parse_args()
document_id, count, duplicate = ingest_bytes(
    args.file.name, args.file.read_bytes()
)
print({"id": str(document_id), "chunks": count, "duplicate": duplicate})