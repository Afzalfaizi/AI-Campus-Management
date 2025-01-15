from fastapi import FastAPI, UploadFile, File, HTTPException
from app.database import create_tables
from app.crud import bulk_import_students
from app.llm import agent
import io

app = FastAPI(
    title="AI College Management System",
    description="A smart college management system with AI-powered chat interface",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    """
    Initialize the application by creating database tables.
    """
    create_tables()

@app.get('/')
def index():
    """
    Root endpoint returning welcome message.
    
    Returns:
        dict: Welcome message
    """
    return {"message": "Welcome to My AI College Management System"}

@app.post("/upload-students/")
async def upload_students(file: UploadFile = File(...)):
    """
    Upload and process a student data file.
    
    Args:
        file (UploadFile): CSV or Excel file containing student data

    Returns:
        dict: Import results including success message and imported students

    Raises:
        HTTPException: If file format is invalid or processing fails
    """
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel files are supported"
        )
    
    content = await file.read()
    file_type = 'csv' if file.filename.endswith('.csv') else 'excel'
    
    try:
        students = bulk_import_students(content, file_type)
        return {
            "message": f"Successfully imported {len(students)} students",
            "students": [{"id": s.id, "roll_no": s.roll_no, "name": s.name} for s in students]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/chat/{query}")
def get_content(query: str):
    """
    Process a chat query using the AI agent.
    
    Args:
        query (str): The user's query

    Returns:
        dict: AI agent's response
    """
    try:
        config = {"configurable": {"thread_id": "2"}}
        result = agent.invoke({"messages": [("user", query)]}, config)
        return result
    except Exception as e:
        return {"error": str(e)}