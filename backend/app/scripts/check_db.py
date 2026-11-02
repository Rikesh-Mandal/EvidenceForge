from sqlalchemy import text
from app.database import engine


with engine.connect() as conn:
    version = conn.execute(text("SELECT version()")).scalar_one()
    print(version.split(",")[0])