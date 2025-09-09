from typing import List, Literal
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Ticket(BaseModel):
    id: int
    property_id: int
    title: str
    status: Literal["open","in_progress","closed"] = "open"

_TICKETS: List[Ticket] = [
    Ticket(id=1, property_id=1, title="Fuite évier", status="open")
]

@router.get("")
def list_tickets():
    return {"items": [t.model_dump() for t in _TICKETS], "count": len(_TICKETS)}
