from fastapi import FastAPI
from app.database import create_tables
from contextlib import asynccontextmanager
from app.llm import agent

# FastAPI app initialization
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()

@app.get('/')
def index():
    return {"message": "Welcome to My AI College Management System"}

# Chat API Endpoint
@app.get("/chat/{query}")
def get_content(query: str):
    """
    Process chat queries and return responses
    Uses a fixed thread_id for demonstration purposes
    """
    try:
        config = {"configurable": {"thread_id": "2"}}
        result = agent.invoke({"messages": [("user", query)]}, config)
        return result
    except Exception as e:
        return {"output": str(e)}