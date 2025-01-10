from sqlmodel import Session
from app.database import engine
from app.models import Student

def add_student(name: str, email: str, phone: str, class_name: str) -> Student:
    """
    Add a new student to the database.
    
    Args:
        name (str): The name of the student.
        email (str): The email of the student.
        phone (str): The phone number of the student.
        class_name (str): The class name of the student.
        

    Returns:
        Student: The created student object.
    """
    student = Student(name=name, email=email, phone=phone, class_name=class_name)
    with Session(engine) as session:
        session.add(student)
        session.commit()
        session.refresh(student)
    return student
