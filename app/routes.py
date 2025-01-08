from fastapi import APIRouter, Depends, HTTPException
from app.models import Student, Teacher, Admin
from app.database import get_session
from app.crud import create_entity, read_entities, update_entity, delete_entity
from app.llm import assistant

router = APIRouter()

@router.post("/students/")
def add_student(name: str, email: str, phone: str, class_name: str, session=Depends(get_session)):
    """
    Adds a new student to the database.

    AI Usage:
        This function is accessed by AI to create a new student record.

    Args:
        name (str): Student's name.
        email (str): Student's email.
        phone (str): Student's phone number.
        class_name (str): Class name the student belongs to.

    Returns:
        dict: Created student record.
    """
    return create_entity(session, Student(name=name, email=email, phone=phone, class_name=class_name))

@router.get("/students/")
def list_students(class_name: str = None, session=Depends(get_session)):
    """
    Retrieves students, optionally filtered by class name.

    AI Usage:
        Used by AI to fetch a list of students or filter them by class.

    Args:
        class_name (str, optional): Class name to filter students.

    Returns:
        list: A list of matching student records.
    """
    filter_by = Student.class_name == class_name if class_name else None
    return read_entities(session, Student, filter_by)

@router.put("/students/{student_id}")
def update_student(student_id: int, updates: dict, session=Depends(get_session)):
    """
    Updates a student's information.

    AI Usage:
        Allows AI to update student details.

    Args:
        student_id (int): ID of the student to update.
        updates (dict): Fields to update.

    Returns:
        dict: Updated student record.
    """
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return update_entity(session, student, updates)

@router.delete("/students/{student_id}")
def delete_student(student_id: int, session=Depends(get_session)):
    """
    Deletes a student record by ID.

    AI Usage:
        Used by AI to remove a student from the database.

    Args:
        student_id (int): ID of the student to delete.

    Returns:
        bool: Whether the deletion was successful.
    """
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return delete_entity(session, student)

@router.get("/chat/{query}")
def chat_with_ai(query: str):
    """
    Handles chat-based queries through AI.

    Args:
        query (str): User's query.

    Returns:
        dict: AI-generated response to the query.
    """
    messages = [("user", query)]
    return assistant(messages)
