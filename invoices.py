
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List
from datetime import datetime

router = APIRouter()

# In-memory store (MVP demo) — replace by DB layer
INVOICES: Dict[int, dict] = {}
SEQ = 1

def _next_id():
    global SEQ
    i = SEQ
    SEQ += 1
    return i

@router.post("")
def create_invoice(lease_id: int, period_ym: str, amount: float, reference: str):
    if len(period_ym) != 7 or period_ym[4] != '-':
        raise HTTPException(400, "period_ym must be 'YYYY-MM'")
    inv_id = _next_id()
    INVOICES[inv_id] = {
        "id": inv_id,
        "lease_id": lease_id,
        "period_ym": period_ym,
        "amount_due": float(amount),
        "reference": reference,
        "status": "due",
        "created_at": datetime.utcnow().isoformat()
    }
    return INVOICES[inv_id]

@router.get("/{invoice_id}")
def get_invoice(invoice_id: int):
    inv = INVOICES.get(invoice_id)
    if not inv:
        raise HTTPException(404, "invoice not found")
    return inv

@router.get("")
def list_invoices(lease_id: int = Query(...)):
    return [inv for inv in INVOICES.values() if inv["lease_id"] == lease_id]

@router.post("/{invoice_id}/mark_paid")
def mark_paid(invoice_id: int, tx_id: str = ""):
    inv = INVOICES.get(invoice_id)
    if not inv:
        raise HTTPException(404, "invoice not found")
    inv["status"] = "paid"
    inv["paid_at"] = datetime.utcnow().isoformat()
    inv["tx_id"] = tx_id
    return inv

@router.get("/{invoice_id}/status")
def invoice_status(invoice_id: int):
    inv = INVOICES.get(invoice_id)
    if not inv:
        raise HTTPException(404, "invoice not found")
    return {"id": inv["id"], "status": inv["status"], "paid_at": inv.get("paid_at")}
