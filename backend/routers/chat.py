from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field

from backend.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])
chat_service = ChatService()


class ChatRequest(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    message: str = Field(..., min_length=1, description="User input text")


class ChatResponse(BaseModel):
    user_id: str
    message: str
    reply: str
    model: str
    latency_ms: float


@router.post("/message", response_model=ChatResponse)
def post_message(payload: ChatRequest = Body(...)) -> ChatResponse:
    """Send a message to the chat service and return the model reply."""

    try:
        return chat_service.send_message(payload.user_id, payload.message)  # type: ignore[return-value]
    except Exception as exc:  # Surface as HTTP 502 for client clarity
        raise HTTPException(status_code=502, detail=str(exc)) from exc
