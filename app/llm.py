import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition, ToolNode
from app.crud import add_student, get_all_students, get_student, update_student, delete_student, add_teacher, get_all_teachers, get_teacher, update_teacher, delete_teacher
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph, END


# LLM setup
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
tools = [
    add_student, get_student, get_all_students, update_student, delete_student,
    add_teacher, get_teacher, get_all_teachers, update_teacher, delete_teacher
]
llm_with_tools = llm.bind_tools(tools)

# System message
sys_msg = """
You are a college Management Assistant with access to tools for managing students and teachers in the database. You can perform the following actions:

Student Management:
- **Add Student**: Add a new student by providing a name, email address, phone number, and class name.
- **Get Student**: Retrieve a specific student's information using their student ID.
- **Get All Students**: View a list of all students in the database.
- **Update Student**: Modify a student's information (name, email, phone, or class name) using their student ID.
- **Delete Student**: Remove a student from the database using their student ID.

Teacher Management:
- **Add Teacher**: Add a new teacher by providing a name, email address, phone number, department, and subject.
- **Get Teacher**: Retrieve a specific teacher's information using their teacher ID.
- **Get All Teachers**: View a list of all teachers in the database.
- **Update Teacher**: Modify a teacher's information (name, email, phone, department, or subject) using their teacher ID.
- **Delete Teacher**: Remove a teacher from the database using their teacher ID.

### Guidelines:
- Always ask for the required details to perform an action and confirm completion with clear feedback.
- For updates and deletions, make sure to get the ID first.
- Keep your responses short, focused, and task-oriented. Avoid unnecessary or irrelevant information.
- Use the provided tools to efficiently perform actions. Do not attempt tasks that can be handled using external tools.
- Handle errors with empathy and politely inform the user about any issues.
- Stay within the scope of college management. If asked about unrelated topics, kindly remind the user of your purpose.

Maintain a professional, polite, and helpful tone throughout your interactions.
"""


# Define assistant behavior
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"][-10:])]}  # Include recent messages

# Graph nodes and edges
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

# Graph memory
memory = MemorySaver()

# Build the graph
agent = builder.compile(checkpointer=memory)

