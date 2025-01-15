import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import MessagesState, StateGraph, START, END
from app.settings import GOOGLE_API_KEY
from app.crud import (
    add_student, get_student, get_all_students, update_student, delete_student,
    search_student_by_roll_no, search_students_by_class_section,
    search_students_by_status, add_teacher, get_teacher, get_all_teachers,
    update_teacher, delete_teacher
)

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

# Configure available tools
tools = [
    add_student, get_student, get_all_students, update_student, delete_student,
    search_student_by_roll_no, search_students_by_class_section, search_students_by_status,
    add_teacher, get_teacher, get_all_teachers, update_teacher, delete_teacher
]

llm_with_tools = llm.bind_tools(tools)

# System message defining AI assistant's capabilities
sys_msg = """
You are a college Management Assistant with access to tools for managing student records. You can perform the following actions:

Student Management:
1. Data Import:
   - Bulk import student records from Excel/CSV files
   - Required fields: roll number, name, DOB, class, section, gender, status, CNIC/B-Form, contact details, etc.

2. Search and Retrieval:
   - Search by Roll Number
   - Search by Class and Section
   - Search by Student Status
   - Get Complete Student Details
   - List All Students

3. Data Fields Available:
   - Student Name
   - Roll Number
   - Date of Birth
   - Class and Section
   - Gender (male/female/other)
   - Current Status (active/inactive/graduated/suspended)
   - CNIC/B-Form Number
   - Contact Information
   - Email Address
   - Father/Guardian Details
   - Permanent Address
   - Religion

4. Teacher Management:
   - Add, Update, Delete Teacher records
   - View Teacher Information
   - List All Teachers

Student Management Operations:
1. Add Student: Provide all required student details
2. Update Student: Update specific fields by student ID
   - All fields are optional for updates
   - Only provided fields will be updated
   - Available fields:
     * roll_no
     * name
     * date_of_birth (YYYY-MM-DD)
     * class_name
     * section
     * gender
     * current_status
     * cnic_or_bform
     * contact_no
     * email
     * father_guardian_name
     * father_guardian_contact
     * father_guardian_cnic
     * permanent_address
     * religion
3. Delete Student: Remove student by ID
4. Search Students:
   - By roll number
   - By class and section
   - By current status

Guidelines:
- Verify all required fields when adding new students
- Ensure proper date format (YYYY-MM-DD) for DOB
- CNIC/B-Form numbers must be unique
- Roll numbers must be unique
- Handle data with confidentiality and proper authorization

Please ask for specific search criteria to help retrieve the exact information needed.
"""

def assistant(state: MessagesState):
    """
    Process messages and generate responses using the LLM.
    
    Args:
        state (MessagesState): Current conversation state

    Returns:
        dict: Generated response messages
    """
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"][-10:])]}

# Configure the graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

# Set up memory
memory = MemorySaver()

# Build the agent
agent = builder.compile(checkpointer=memory)

