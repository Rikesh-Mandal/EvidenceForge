"""HNSW cosine index. Revision ID: 0002_hnsw; Revises: 0001_initial."""
from alembic import op


revision = "0002_hnsw"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade():
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_chunks_embedding_hnsw "
        "ON chunks USING hnsw (embedding vector_cosine_ops)"
    )


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_chunks_embedding_hnsw")