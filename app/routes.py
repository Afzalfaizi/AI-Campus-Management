from fastapi import APIRouter
from app.llm import assistant
from langgraph.graph import MessagesState

router = APIRouter()

@router.post("/chat/")
def chat_with_ai(query: str):
    """
    Process user queries via chat and delegate actions to tools.
    """
    try:
        state = MessagesState(messages=[("user", query)])
        response = assistant(state)
        if "messages" in response:
            return {"message": response["messages"][0]["content"]}
        else:
            return {"message": "No response from AI. Please try again."}
    except Exception as e:
        return {"error": str(e)}
