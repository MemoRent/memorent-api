from fastapi import APIRouter

router = APIRouter()

@router.get("")
def list_invoices():
    return {"invoices": []}

@router.post("")
def create_invoice():
    return {"message": "create invoice (stub)"}

    inv = INVOICES.get(invoice_id)
    if not inv:
        raise HTTPException(404, "invoice not found")
    return {"id": inv["id"], "status": inv["status"], "paid_at": inv.get("paid_at")}
