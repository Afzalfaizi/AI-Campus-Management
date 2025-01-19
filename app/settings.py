from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI").replace("postgresql", "postgresql+psycopg")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
OAUTH_REDIRECT_URL = os.getenv("OAUTH_REDIRECT_URL", "http://localhost:8000/auth/callback")
