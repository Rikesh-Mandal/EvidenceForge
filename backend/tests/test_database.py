from sqlalchemy import select, text
from app.database import SessionLocal
from app.models import Document
def test_pgvector_extension_is_installed():
    with SessionLocal() as session:
        name = session.execute(
            text("SELECT extname FROM pg_extension WHERE extname = 'vector'")
        ).scalar_one()
    assert name == "vector"
def test_database_can_query_documents():
    with SessionLocal() as session:
        result = session.execute(select(Document).limit(1))
        rows = result.all()
        assert isinstance(rows, list)