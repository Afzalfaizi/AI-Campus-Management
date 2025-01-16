import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI").replace("postgresql", "postgresql+psycopg")

# Database engine
engine = create_engine(DATABASE_URI, connect_args={"sslmode": "require"})

def create_tables():
    """
    Create all database tables based on SQLModel classes.
    This function drops existing tables and creates new ones.
    """
    try:
        # # Drop all existing tables
        # SQLModel.metadata.drop_all(engine)
        # Create new tables
        SQLModel.metadata.create_all(engine)
        print("Tables created successfully")
    except Exception as e:
        raise Exception(f"Failed to create database tables: {str(e)}")
