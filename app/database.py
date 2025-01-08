from sqlmodel import create_engine, Session
from app.settings import DATABASE_URI
from app.models import SQLModel

# Database Engine
engine = create_engine(DATABASE_URI, connect_args={"sslmode": "require"})

# Create Tables
def create_tables():
    SQLModel.metadata.create_all(engine)

# Session Dependency
def get_session():
    with Session(engine) as session:
        yield session
