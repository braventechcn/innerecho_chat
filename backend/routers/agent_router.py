from fastapi import APIRouter, Body

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/run")
def run_agent(user_id: str = Body(...), query: str = Body(...)) -> dict:
    """Agent execution stub."""
    return {"user_id": user_id, "query": query, "result": "pending"}
