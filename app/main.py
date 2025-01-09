from fastapi import FastAPI
from app.routes import router
from app.database import create_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    """
    Initialize the database and create tables on app startup.
    """
    create_tables()

app.include_router(router)

@app.get("/")
def root():
    """
    Root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the College Management System. Use the /chat endpoint for queries."}
