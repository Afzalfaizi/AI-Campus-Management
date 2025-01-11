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

def get_student(student_id: int) -> Student | None:
    """
    Get a student from the database by ID.
    
    Args:
        student_id (int): The ID of the student to retrieve.

    Returns:
        Student | None: The student object if found, None otherwise.
    """
    with Session(engine) as session:
        return session.get(Student, student_id)

def get_all_students() -> list[Student]:
    """
    Get all students from the database.
    
    Returns:
        list[Student]: List of all student objects.
    """
    with Session(engine) as session:
        return session.query(Student).all()

def update_student(student_id: int, name: str | None = None, email: str | None = None, 
                  phone: str | None = None, class_name: str | None = None) -> Student | None:
    """
    Update a student's information in the database.
    
    Args:
        student_id (int): The ID of the student to update.
        name (str, optional): The new name of the student.
        email (str, optional): The new email of the student.
        phone (str, optional): The new phone number of the student.
        class_name (str, optional): The new class name of the student.

    Returns:
        Student | None: The updated student object if found, None otherwise.
    """
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if student:
            if name is not None:
                student.name = name
            if email is not None:
                student.email = email
            if phone is not None:
                student.phone = phone
            if class_name is not None:
                student.class_name = class_name
            session.commit()
            session.refresh(student)
        return student

def delete_student(student_id: int) -> bool:
    """
    Delete a student from the database.
    
    Args:
        student_id (int): The ID of the student to delete.

    Returns:
        bool: True if student was deleted, False if student was not found.
    """
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if student:
            session.delete(student)
            session.commit()
            return True
        return False
