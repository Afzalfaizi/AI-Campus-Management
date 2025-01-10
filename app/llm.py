import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition, ToolNode
from app.crud import add_student
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph, END


# LLM setup
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
tools = [add_student]
llm_with_tools = llm.bind_tools(tools)
# System message
sys_msg = """
You are a college Management Assistant with access to tools for managing adding students in database. You can perform the following actions:

- **add student Todo**: Add a new students by providing a name, an email address, phone number, and class name.

### Guidelines:
- Always ask for the required details to perform an action and confirm completion with clear feedback.
- Keep your responses short, focused, and task-oriented. Avoid unnecessary or irrelevant information.
- Use the provided tools to efficiently perform actions. Do not attempt tasks that can be handled using external tools.
- Handle errors with empathy and politely inform the user about any issues.
- Stay within the scope of todo management. If asked about unrelated topics, kindly remind the user of your purpose and steer the conversation back to college management.

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

