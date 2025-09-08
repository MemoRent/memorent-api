from fastapi import APIRouter
router = APIRouter()

@router.get("/summary")
def summary():
    return {"paid": 2, "overdue": 1, "open_tickets": 1}