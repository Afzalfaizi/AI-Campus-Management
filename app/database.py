import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI").replace("postgresql", "postgresql+psycopg")

# Database engine
engine = create_engine(DATABASE_URI, connect_args={"sslmode": "require"})

def create_tables():
    SQLModel.metadata.create_all(engine)
