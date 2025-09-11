
from fastapi import APIRouter, Request
from typing import List, Dict
from invoices import INVOICES

router = APIRouter()

def _normalize(s: str) -> str:
    return (s or '').upper().replace(' ', '').replace('/', '')

@router.post("/bank/transactions")
async def bank_transactions(req: Request):
    body = await req.json()
    txs: List[Dict] = body.get("transactions", [])
    matched = []
    for tx in txs:
        amount = float(tx.get("amount", 0))
        currency = (tx.get("currency") or "EUR").upper()
        remi = _normalize(tx.get("remittanceInformation", ""))

        invoice = next(
            (v for v in INVOICES.values()
             if _normalize(v.get('reference', '')) in remi),
            None
        )

        if invoice:
            inv_currency = (invoice.get('currency') or 'EUR').upper()
            if inv_currency == currency and abs(float(invoice['amount_due']) - amount) <= 0.01:
                invoice['status'] = 'paid'
                invoice['paid_at'] = tx.get('bookingDate')
                invoice['tx_id'] = tx.get('transactionId')
                matched.append(invoice['id'])

    return {"matched": matched, "received": len(txs)}
