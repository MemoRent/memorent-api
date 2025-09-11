
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter()

# Store minimal pour la beta (remplaçable ensuite par la DB)
INVOICES: Dict[str, Dict[str, Any]] = {
    # EXEMPLE (tu peux le retirer si tu veux démarrer vide)
    "INV-2025-0001": {
        "id": "INV-2025-0001",
        "reference": "+++123456789012+++",  # communication structurée
        "amount_due": 125.00,
        "currency": "EUR",
        "status": "open",
        "paid_at": None,
        "tx_id": None,
    }
}

@router.get("")
def list_invoices():
    return {"invoices": list(INVOICES.values())}

@router.get("/{invoice_id}")
def get_invoice(invoice_id: str):
    inv = INVOICES.get(invoice_id)
    if not inv:
        raise HTTPException(404, "invoice not found")
    return inv

@router.post("")
def create_invoice(invoice: Dict[str, Any]):
    inv_id = invoice.get("id")
    if not inv_id:
        raise HTTPException(400, "missing id")
    INVOICES[inv_id] = {
        "id": inv_id,
        "reference": invoice.get("reference", ""),
        "amount_due": float(invoice.get("amount_due", 0)),
        "currency": (invoice.get("currency") or "EUR").upper(),
        "status": "open",
        "paid_at": None,
        "tx_id": None,
    }
    return {"ok": True, "id": inv_id}
