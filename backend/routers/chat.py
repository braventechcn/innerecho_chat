from fastapi import APIRouter, Body

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/message")
def post_message(user_id: str = Body(...), message: str = Body(...)) -> dict:
    """Chat entrypoint stub."""
    return {"user_id": user_id, "echo": message}
