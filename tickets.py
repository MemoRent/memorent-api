from fastapi import APIRouter, Path
router = APIRouter()

@router.get("")
def list_tickets():
    return {"tickets": []}

@router.post("")
def create_ticket():
    return {"message": "ticket created (stub)"}

@router.patch("/{ticket_id}")
def update_ticket(ticket_id: int = Path(..., ge=1)):
    return {"message": f"ticket {ticket_id} updated (stub)"}