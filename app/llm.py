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
from app.models import UserRole

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

# Configure available tools
tools = [
    add_student, get_student, get_all_students, update_student, delete_student,
    search_student_by_roll_no, search_students_by_class_section, search_students_by_status,
    add_teacher, get_teacher, get_all_teachers, update_teacher, delete_teacher
]

llm_with_tools = llm.bind_tools(tools)

def get_role_specific_system_message(user_role: UserRole) -> str:
    """Get role-specific system message."""
    base_msg = "You are a college Management Assistant. "
    
    if user_role == UserRole.ADMIN:
        return base_msg + """
        You have full administrative access to:
        - Manage all student records
        - Manage all teacher records
        - View and modify system settings
        """
    elif user_role == UserRole.TEACHER:
        return base_msg + """
        You have access to:
        - View your assigned students
        - Update grades and attendance
        - View your own profile
        """
    else:  # STUDENT
        return base_msg + """
        You have access to:
        - View your own academic records
        - View your attendance
        - Update your contact information , view you class Schedule
        """

def assistant(state: MessagesState):
    """Process messages based on user role."""
    user_role = state.get("configurable", {}).get("user_role", UserRole.STUDENT)
    system_message = get_role_specific_system_message(user_role)
    return {"messages": [llm_with_tools.invoke([system_message] + state["messages"][-10:])]}

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

