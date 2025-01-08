from fastapi import FastAPI
from app.routes import router
from app.database import create_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to the College Management System"}
