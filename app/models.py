from sqlmodel import SQLModel, Field

class Student(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
    class_name: str
    grades: str = None

class Teacher(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    subject: str
    phone: str

class Admin(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
