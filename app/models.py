from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import date

class Gender(str, Enum):
    """
    Enumeration for student gender options.
    """
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class StudentStatus(str, Enum):
    """
    Enumeration for student status options.
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    GRADUATED = "graduated"
    SUSPENDED = "suspended"

class Student(SQLModel, table=True):
    """
    Student model representing the students table in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    roll_no: str = Field(unique=True, index=True)
    name: str
    date_of_birth: date
    class_name: str
    section: str
    gender: Gender
    current_status: StudentStatus = Field(default=StudentStatus.ACTIVE)
    cnic_or_bform: str = Field(unique=True)
    contact_no: str
    email: str
    father_guardian_name: str
    father_guardian_contact: str
    father_guardian_cnic: str
    permanent_address: str
    religion: str

class Teacher(SQLModel, table=True):
    """
    Teacher model representing the teachers table in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
    department: str
    subject: str
