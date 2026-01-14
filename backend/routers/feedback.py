from fastapi import APIRouter, Body

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("")
def submit_feedback(user_id: str = Body(...), rating: int = Body(...), comment: str | None = Body(None)) -> dict:
    """Collect user feedback stub."""
    return {"user_id": user_id, "rating": rating, "comment": comment}
