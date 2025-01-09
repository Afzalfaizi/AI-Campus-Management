from langchain_google_genai import ChatGoogleGenerativeAI
from app.settings import GOOGLE_API_KEY
from app.crud import create_student, read_students, update_student, delete_student

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

tools = [
    {
        "name": "create_student",  # Tool name must match the system message description
        "function": create_student,
        "parameters": {
            "name": {"type": "string", "description": "Name of the student"},
            "email": {"type": "string", "description": "Email address of the student"},
            "phone": {"type": "string", "description": "Phone number of the student"},
            "class_name": {"type": "string", "description": "Class of the student"},
        },
    },
    {
        "name": "read_students",
        "function": read_students,
        "parameters": {
            "filter_by": {
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "value": {"type": "string"},
                },
                "optional": True,
            },
        },
    },
    {
        "name": "update_student",
        "function": update_student,
        "parameters": {
            "student_id": {"type": "integer"},
            "updates": {
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "value": {"type": "string"},
                },
                "required": ["key", "value"],
            },
        },
    },
    {
        "name": "delete_student",
        "function": delete_student,
        "parameters": {
            "student_id": {"type": "integer"},
        },
    },
]

llm_with_tools = llm.bind_tools(tools)

sys_msg = """
You are a College Management Assistant specializing in managing students. You can:
- Add a student by specifying their name, email, phone, and class.
- List all students or filter them by criteria like class.
- Update a student's details.
- Delete a student by their ID.

### Example Queries:
- "Add a student named Sarah in class 12B with email sarah@example.com and phone 98765."
- "List all students in class 12B."
- "Update student 1's email to newemail@example.com."
- "Delete student with ID 1."
"""

def assistant(state):
    """
    Process queries and delegate actions to tools.
    """
    ai_response = llm_with_tools.invoke([sys_msg] + state["messages"])
    return {"messages": [{"content": ai_response.content}]}
