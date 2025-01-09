from sqlmodel import create_engine, SQLModel
from app.settings import DATABASE_URI

engine = create_engine(DATABASE_URI, connect_args={"sslmode": "require"})

def create_tables():
    """
    Create tables in the database.
    """
    SQLModel.metadata.create_all(engine)
