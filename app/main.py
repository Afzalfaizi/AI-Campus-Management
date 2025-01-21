from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from datetime import timedelta
from app.database import create_tables, engine
from app.models import User, UserRole
from app.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token,
    get_current_user, check_admin_access, check_teacher_access,
    verify_password, oauth, get_password_hash
)
from app.crud import (
    add_student, get_student, get_all_students,
    update_student, delete_student, bulk_import_students
)
from app.llm import agent
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field
from typing import Optional

app = FastAPI(
    title="AI College Management System",
    description="A smart college management system with AI langraph-powered chat interface and OAuth authentication",
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

@app.post("/register")
async def register(username: str, email: str, password: str, role: UserRole):
    """User registration endpoint."""
    if role not in [UserRole.ADMIN, UserRole.TEACHER, UserRole.STUDENT]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be 'admin', 'teacher', or 'student'."
        )

    with Session(engine) as session:
        # Check if the user already exists
        existing_user = session.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered try with other username or email"
            )
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            role=role  # Set the role based on user input
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        return {"message": "User registered successfully", "user_id": new_user.id}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint for username/password authentication."""
    with Session(engine) as session:
        user = session.query(User).filter(User.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

@app.get('/login/google')
async def google_login(request: Request):
    """Initialize Google OAuth login."""
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/auth/callback')
async def auth_callback(request: Request):
    """Handle OAuth callback."""
    token = await oauth.google.authorize_access_token(request)
    user = await get_oauth_user("google", token)
    if user:
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate OAuth credentials",
    )

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user

@app.get("/chat/{query}")
async def get_chat_response(
    query: str,
    current_user: User = Depends(get_current_user)
):
    """Process chat query with AI agent."""
    try:
        config = {
            "configurable": {
                "thread_id": "2",
                "user_role": current_user.role
            }
        }
        result = agent.invoke({"messages": [("user", query)]}, config)
        return result
    except Exception as e:
        return {"error": str(e)}

# Protected admin routes
@app.get("/admin/users", dependencies=[Depends(check_admin_access)])
async def get_all_users():
    """Admin endpoint to get all users."""
    with Session(engine) as session:
        return session.query(User).all()

# Protected teacher routes
@app.get("/teacher/students", dependencies=[Depends(check_teacher_access)])
async def get_teacher_students(current_user: User = Depends(get_current_user)):
    """Teacher endpoint to get their students."""
    # Implement based on your requirements
    pass