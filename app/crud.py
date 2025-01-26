from sqlmodel import Session
from typing import List
import pandas as pd
from datetime import datetime, date
from fastapi import HTTPException
from app.database import engine
from app.models import Student, Teacher, StudentStatus, Gender, User, UserRole
from app.utils import get_password_hash

def add_student(
    roll_no: str,
    name: str,
    date_of_birth: date,
    class_name: str,
    section: str,
    gender: str,
    cnic_or_bform: str,
    contact_no: str,
    email: str,
    father_guardian_name: str,
    father_guardian_contact: str,
    father_guardian_cnic: str,
    permanent_address: str,
    religion: str,
    current_status: str = StudentStatus.ACTIVE
) -> Student:
    """
    Add a new student to the database.
    
    Args:
        roll_no (str): Unique roll number for the student
        name (str): Full name of the student
        date_of_birth (date): Date of birth
        class_name (str): Class name
        section (str): Section
        gender (str): Gender (male/female/other)
        cnic_or_bform (str): CNIC or B-Form number
        contact_no (str): Contact number
        email (str): Email address
        father_guardian_name (str): Name of father or guardian
        father_guardian_contact (str): Contact of father or guardian
        father_guardian_cnic (str): CNIC of father or guardian
        permanent_address (str): Permanent address
        religion (str): Religion
        current_status (str, optional): Current status. Defaults to ACTIVE.

    Returns:
        Student: Created student object
    """
    student = Student(
        roll_no=roll_no,
        name=name,
        date_of_birth=date_of_birth,
        class_name=class_name,
        section=section,
        gender=gender,
        cnic_or_bform=cnic_or_bform,
        contact_no=contact_no,
        email=email,
        father_guardian_name=father_guardian_name,
        father_guardian_contact=father_guardian_contact,
        father_guardian_cnic=father_guardian_cnic,
        permanent_address=permanent_address,
        religion=religion,
        current_status=current_status
    )
    with Session(engine) as session:
        session.add(student)
        session.commit()
        session.refresh(student)
    return student

def get_student(student_id: int) -> Student | None:
    """
    Get a student by their ID.
    
    Args:
        student_id (int): The ID of the student

    Returns:
        Student | None: The student object if found, None otherwise
    """
    with Session(engine) as session:
        return session.get(Student, student_id)

def get_all_students() -> List[Student]:
    """
    Get all students from the database.
    
    Returns:
        List[Student]: List of all student objects
    """
    with Session(engine) as session:
        return session.query(Student).all()

def search_student_by_roll_no(roll_no: str) -> Student | None:
    """
    Search for a student by their roll number.
    
    Args:
        roll_no (str): The roll number to search for

    Returns:
        Student | None: The student object if found, None otherwise
    """
    with Session(engine) as session:
        return session.query(Student).filter(Student.roll_no == roll_no).first()

def search_students_by_class_section(class_name: str, section: str) -> List[Student]:
    """
    Search for students by class and section.
    
    Args:
        class_name (str): The class name
        section (str): The section

    Returns:
        List[Student]: List of matching student objects
    """
    with Session(engine) as session:
        return session.query(Student).filter(
            Student.class_name == class_name,
            Student.section == section
        ).all()

def search_students_by_status(status: StudentStatus) -> List[Student]:
    """
    Search for students by their current status.
    
    Args:
        status (StudentStatus): The status to search for

    Returns:
        List[Student]: List of matching student objects
    """
    with Session(engine) as session:
        return session.query(Student).filter(Student.current_status == status).all()

def update_student(
    student_id: int,
    roll_no: str | None = None,
    name: str | None = None,
    date_of_birth: date | None = None,
    class_name: str | None = None,
    section: str | None = None,
    gender: str | None = None,
    current_status: str | None = None,
    cnic_or_bform: str | None = None,
    contact_no: str | None = None,
    email: str | None = None,
    father_guardian_name: str | None = None,
    father_guardian_contact: str | None = None,
    father_guardian_cnic: str | None = None,
    permanent_address: str | None = None,
    religion: str | None = None
) -> Student | None:
    """
    Update a student's information.
    
    Args:
        student_id (int): The ID of the student to update
        roll_no (str, optional): New roll number
        name (str, optional): New name
        date_of_birth (date, optional): New date of birth
        class_name (str, optional): New class name
        section (str, optional): New section
        gender (str, optional): New gender
        current_status (str, optional): New status
        cnic_or_bform (str, optional): New CNIC or B-Form number
        contact_no (str, optional): New contact number
        email (str, optional): New email address
        father_guardian_name (str, optional): New father/guardian name
        father_guardian_contact (str, optional): New father/guardian contact
        father_guardian_cnic (str, optional): New father/guardian CNIC
        permanent_address (str, optional): New permanent address
        religion (str, optional): New religion

    Returns:
        Student | None: Updated student object if found, None otherwise
    """
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if student:
            # Update only the provided fields
            if roll_no is not None:
                student.roll_no = roll_no
            if name is not None:
                student.name = name
            if date_of_birth is not None:
                student.date_of_birth = date_of_birth
            if class_name is not None:
                student.class_name = class_name
            if section is not None:
                student.section = section
            if gender is not None:
                student.gender = gender
            if current_status is not None:
                student.current_status = current_status
            if cnic_or_bform is not None:
                student.cnic_or_bform = cnic_or_bform
            if contact_no is not None:
                student.contact_no = contact_no
            if email is not None:
                student.email = email
            if father_guardian_name is not None:
                student.father_guardian_name = father_guardian_name
            if father_guardian_contact is not None:
                student.father_guardian_contact = father_guardian_contact
            if father_guardian_cnic is not None:
                student.father_guardian_cnic = father_guardian_cnic
            if permanent_address is not None:
                student.permanent_address = permanent_address
            if religion is not None:
                student.religion = religion
            
            session.commit()
            session.refresh(student)
        return student

def delete_student(student_id: int) -> bool:
    """
    Delete a student from the database.
    
    Args:
        student_id (int): The ID of the student to delete

    Returns:
        bool: True if deleted successfully, False if student not found
    """
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if student:
            session.delete(student)
            session.commit()
            return True
        return False

def bulk_import_students(file_content: bytes, file_type: str) -> List[Student]:
    """
    Import multiple students from a file.
    
    Args:
        file_content (bytes): The file content
        file_type (str): Type of file ('csv' or 'excel')

    Returns:
        List[Student]: List of created student objects

    Raises:
        HTTPException: If there are any validation or processing errors
    """
    try:
        if file_type == 'csv':
            df = pd.read_csv(pd.io.common.BytesIO(file_content))
        else:
            df = pd.read_excel(pd.io.common.BytesIO(file_content))
        
        required_columns = [
            'roll_no', 'name', 'date_of_birth', 'class_name', 'section',
            'gender', 'current_status', 'cnic_or_bform', 'contact_no',
            'email', 'father_guardian_name', 'father_guardian_contact',
            'father_guardian_cnic', 'permanent_address', 'religion'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        students = []
        with Session(engine) as session:
            for _, row in df.iterrows():
                try:
                    dob = datetime.strptime(str(row['date_of_birth']), '%Y-%m-%d').date()
                    
                    student = Student(
                        roll_no=str(row['roll_no']),
                        name=str(row['name']),
                        date_of_birth=dob,
                        class_name=str(row['class_name']),
                        section=str(row['section']),
                        gender=row['gender'].lower(),
                        current_status=row['current_status'].lower(),
                        cnic_or_bform=str(row['cnic_or_bform']),
                        contact_no=str(row['contact_no']),
                        email=str(row['email']),
                        father_guardian_name=str(row['father_guardian_name']),
                        father_guardian_contact=str(row['father_guardian_contact']),
                        father_guardian_cnic=str(row['father_guardian_cnic']),
                        permanent_address=str(row['permanent_address']),
                        religion=str(row['religion'])
                    )
                    session.add(student)
                    students.append(student)
                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Error processing row {_+2}: {str(e)}"
                    )
            
            session.commit()
            for student in students:
                session.refresh(student)
        
        return students
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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

def add_admin(username: str, email: str, password: str) -> User:
    """
    Add a new admin to the database.
    
    Args:
        username (str): Unique username for the admin
        email (str): Email address of the admin
        password (str): Password for the admin

    Returns:
        User: Created admin user object
    """
    new_user = User(
        username=username,
        email=email,
        hashed_password=get_password_hash(password),
        role=UserRole.ADMIN  # Set the role as ADMIN
    )
    with Session(engine) as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user
