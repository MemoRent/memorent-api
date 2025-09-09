from fastapi import APIRouter
from invoices import _INVOICES
from tickets import _TICKETS

router = APIRouter()

@router.get("/summary")
def summary():
    paid = sum(1 for i in _INVOICES if i.status == "paid")
    overdue = sum(1 for i in _INVOICES if i.status == "due")
    open_tickets = sum(1 for t in _TICKETS if t.status in ("open", "in_progress"))
    return {"paid": paid, "overdue": overdue, "open_tickets": open_tickets}
