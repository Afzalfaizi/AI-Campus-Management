from sqlmodel import Session
from app.database import engine
from app.models import Student

def create_student(name: str, email: str, phone: str, class_name: str) -> dict:
    """
    Add a new student to the database.
    """
    student = Student(name=name, email=email, phone=phone, class_name=class_name)
    with Session(engine) as session:
        session.add(student)
        session.commit()
        session.refresh(student)
    return student.dict()

def read_students(filter_by: dict = None) -> list[dict]:
    """
    Retrieve students from the database.
    """
    with Session(engine) as session:
        query = session.query(Student)
        if filter_by:
            for key, value in filter_by.items():
                query = query.filter(getattr(Student, key) == value)
        return [student.dict() for student in query.all()]

def update_student(student_id: int, updates: dict) -> dict:
    """
    Update an existing student's details.
    """
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} not found.")
        for key, value in updates.items():
            setattr(student, key, value)
        session.add(student)
        session.commit()
        session.refresh(student)
    return student.dict()

def delete_student(student_id: int) -> bool:
    """
    Delete a student from the database.
    """
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            return False
        session.delete(student)
        session.commit()
    return True
