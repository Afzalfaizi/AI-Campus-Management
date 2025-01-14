from sqlmodel import Session
from app.database import engine
from app.models import Student, Teacher

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

def add_teacher(name: str, email: str, phone: str, department: str, subject: str) -> Teacher:
    """
    Add a new teacher to the database.
    """
    teacher = Teacher(name=name, email=email, phone=phone, department=department, subject=subject)
    with Session(engine) as session:
        session.add(teacher)
        session.commit()
        session.refresh(teacher)
    return teacher

def get_teacher(teacher_id: int) -> Teacher | None:
    """
    Get a teacher from the database by ID.
    """
    with Session(engine) as session:
        return session.get(Teacher, teacher_id)

def get_all_teachers() -> list[Teacher]:
    """
    Get all teachers from the database.
    """
    with Session(engine) as session:
        return session.query(Teacher).all()

def update_teacher(teacher_id: int, name: str | None = None, email: str | None = None,
                  phone: str | None = None, department: str | None = None, 
                  subject: str | None = None) -> Teacher | None:
    """
    Update a teacher's information in the database.
    """
    with Session(engine) as session:
        teacher = session.get(Teacher, teacher_id)
        if teacher:
            if name is not None:
                teacher.name = name
            if email is not None:
                teacher.email = email
            if phone is not None:
                teacher.phone = phone
            if department is not None:
                teacher.department = department
            if subject is not None:
                teacher.subject = subject
            session.commit()
            session.refresh(teacher)
        return teacher

def delete_teacher(teacher_id: int) -> bool:
    """
    Delete a teacher from the database.
    """
    with Session(engine) as session:
        teacher = session.get(Teacher, teacher_id)
        if teacher:
            session.delete(teacher)
            session.commit()
            return True
        return False
