from fastapi import APIRouter, Query
from typing import Optional
from utils import ... be_structured_build, be_structured_check, iso11649_rf_check, epc_payload

router = APIRouter()

@router.post("/intent")
def create_payment_intent():
    # Placeholder for PSP flow (Stripe/Mollie) if needed
    return {"payment_intent_id": "pi_stub", "status": "requires_payment_method"}

@router.get("/reference/be")
def generate_be_structured(core10: str = Query(..., regex=r"^\d{10}$")):
    """Generate a Belgian structured communication +++xxxxxxxxxxxx+++ from a 10-digit base."""
    ref = be_structured_build(core10)
    return {"reference": ref}

@router.get("/reference/check")
def check_reference(ref: str):
    """Check if reference is valid (BE structured or ISO11649 RF)."""
    valid_be = be_structured_check(ref)
    valid_rf = iso11649_rf_check(ref) if not valid_be else False
    return {"valid": valid_be or valid_rf, "type": "BE" if valid_be else ("RF" if valid_rf else "UNKNOWN")}

@router.get("/epc_qr_payload")
def get_epc_qr_payload(
    creditor_name: str,
    iban: str,
    amount: float,
    bic: Optional[str] = None,
    purpose: Optional[str] = None,
    reference: Optional[str] = None,
    remittance: Optional[str] = None,
):
    """Return EPC069-12 textual payload for SEPA QR."""
    payload = epc_payload(
        creditor_name=creditor_name,
        iban=iban,
        amount_eur=amount,
        bic=bic or '',
        purpose=purpose or '',
        reference=reference or '',
        remittance=remittance or '',
    )
    return {"payload": payload}
