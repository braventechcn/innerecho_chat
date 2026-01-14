from fastapi import APIRouter, Body

router = APIRouter(prefix="/memory", tags=["memory"])


@router.post("/save")
def save_memory(user_id: str = Body(...), content: dict = Body(...)) -> dict:
    """Save memory stub."""
    return {"user_id": user_id, "status": "saved", "content": content}


@router.get("/load")
def load_memory(user_id: str) -> dict:
    """Load memory stub."""
    return {"user_id": user_id, "memories": []}
