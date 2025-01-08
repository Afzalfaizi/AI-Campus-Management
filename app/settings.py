from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI").replace("postgresql", "postgresql+psycopg")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
