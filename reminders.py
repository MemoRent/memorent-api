
from fastapi import APIRouter, HTTPException, Query
from datetime import date, datetime, timedelta
from typing import List, Dict
from .invoices import INVOICES
from ..templates import REMINDER_TEMPLATES

router = APIRouter()

def _fmt_amount(v: float) -> str:
    return f"{v:,.2f}".replace(',', ' ').replace('.', ',')

def _render(locale: str, typ: str, ctx: Dict[str, str]) -> str:
    tpl = REMINDER_TEMPLATES.get(locale, REMINDER_TEMPLATES['fr']).get(typ)
    return tpl.format(**ctx)

@router.get("/preview")
def preview(invoice_id: int, locale: str = "fr", kind: str = Query("before", enum=["before","due","after"])):
    inv = INVOICES.get(invoice_id)
    if not inv:
        raise HTTPException(404, "invoice not found")
    # infer due_date from inv
    due = inv.get("due_date", None)
    if not due:
        raise HTTPException(400, "invoice has no due_date")
    ctx = {
        "period": inv["period_ym"],
        "amount": _fmt_amount(inv["amount_due"]),
        "due_date": due,
        "reference": inv["reference"],
    }
    body = _render(locale, kind, ctx)
    return {"locale": locale, "kind": kind, "body": body}

@router.post("/run")
def run(today: str = None, locale_default: str = "fr"):
    """Compute which reminders should be sent today and return payloads.
    In production: schedule daily at 09:00 (agency time)."""
    d = date.fromisoformat(today) if today else date.today()
    to_send: List[Dict] = []

    # Default schedule: J-3, J-1, J0, J+1, J+3, J+10
    BEFORE = {-3: "before", -1: "before"}
    AFTER = {1: "after", 3: "after", 10: "after"}

    for inv in INVOICES.values():
        if inv.get("status") == "paid":
            continue
        due_str = inv.get("due_date")
        if not due_str:
            continue
        due = date.fromisoformat(due_str)
        delta = (d - due).days  # negative => before due date
        kind = None
        if delta == 0:
            kind = "due"
        elif delta in BEFORE:
            kind = "before"
        elif delta in AFTER:
            kind = "after"
        if not kind:
            continue

        ctx = {
            "period": inv["period_ym"],
            "amount": _fmt_amount(inv["amount_due"]),
            "due_date": inv["due_date"],
            "reference": inv["reference"],
        }
        body = _render(locale_default, kind, ctx)
        # In production: push to email/SMS dispatcher and insert in reminder_logs
        to_send.append({
            "invoice_id": inv["id"],
            "lease_id": inv["lease_id"],
            "due_date": inv["due_date"],
            "channel": "email",
            "locale": locale_default,
            "kind": kind,
            "subject": body.split("\n\n",1)[0].replace("Objet: ","").replace("Onderwerp: ","").replace("Subject: ",""),
            "body": body,
        })
    return {"date": d.isoformat(), "count": len(to_send), "reminders": to_send}
