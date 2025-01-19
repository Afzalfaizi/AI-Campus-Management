from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum
from datetime import date, datetime

class Gender(str, Enum):
    """
    Enumeration for gender options.
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

class UserRole(str, Enum):
    """
    Enumeration for user roles.
    """
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class User(SQLModel, table=True):
    """
    User model for authentication and authorization.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    role: UserRole
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None
    
    # Relationships
    student: Optional["Student"] = Relationship(back_populates="user")
    teacher: Optional["Teacher"] = Relationship(back_populates="user")

class Student(SQLModel, table=True):
    """
    Student model representing the students table.
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
    
    # Relationships
    user_id: Optional[int] = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="student")

class Teacher(SQLModel, table=True):
    """
    Teacher model representing the teachers table.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
    department: str
    subject: str
    
    # Relationships
    user_id: Optional[int] = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="teacher")
