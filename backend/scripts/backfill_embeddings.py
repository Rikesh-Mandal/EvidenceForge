from sqlalchemy import select
from app.database import SessionLocal
from app.embeddings import encode_passages
from app.models import Chunk


BATCH_SIZE = 32
processed = 0
while True:
    with SessionLocal.begin() as session:
        rows = session.scalars(
            select(Chunk).where(Chunk.embedding.is_(None))
            .order_by(Chunk.id).limit(BATCH_SIZE)
        ).all()
        if not rows:
            break

        vectors = encode_passages([row.content for row in rows])
        for row, embedding in zip(rows, vectors):
            row.embedding = embedding
        processed += len(rows)
        print("Embedded", processed, "chunks")
print("Complete:", processed)
