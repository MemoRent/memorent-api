from fastapi import APIRouter, Request
from typing import List, Dict
from .invoices import INVOICES

router = APIRouter()

def _normalize(s: str) -> str:
    return (s or '').upper().replace(' ', '').replace('/', '')

@router.post("/bank/transactions")
async def bank_transactions(req: Request):
    """Webhook called by your AISP aggregator with new credited transactions."""
    body = await req.json()
    txs: List[Dict] = body.get("transactions", [])
    matched = []
    for tx in txs:
        amount = float(tx.get("amount", 0))
        currency = tx.get("currency", "EUR")
        remi = _normalize(tx.get("remittanceInformation", ""))
        # Try to find invoice by reference contained in remittance
        invoice = next((v for v in INVOICES.values() if v['reference'].replace(' ','').replace('/','').upper() in remi), None)
        if invoice and currency == 'EUR' and abs(invoice['amount_due'] - amount) <= 0.01:
            invoice['status'] = 'paid'
            invoice['paid_at'] = tx.get('bookingDate')
            invoice['tx_id'] = tx.get('transactionId')
            matched.append(invoice['id'])
    return {"matched": matched, "received": len(txs)}