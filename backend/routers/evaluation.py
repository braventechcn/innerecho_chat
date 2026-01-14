from fastapi import APIRouter, Body

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


@router.post("/score")
def score_response(user_id: str = Body(...), response: str = Body(...)) -> dict:
    """Evaluate response stub."""
    return {"user_id": user_id, "score": 0.0, "response": response}
