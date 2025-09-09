
def normalize_ref(s: str) -> str:
    return (s or "").upper().replace(" ", "").replace("/", "")

def be_structured_build(core10: str) -> str:
    """Construit une communication structurée belge +++XXXXXXXXXXYY+++ à partir de 10 chiffres."""
    if not (isinstance(core10, str) and core10.isdigit() and len(core10) == 10):
        raise ValueError("core10 must be a 10-digit string")
    rem = int(core10) % 97
    if rem == 0:
        rem = 97
    return f"+++{core10}{rem:02d}+++"

def be_structured_check(ref: str) -> bool:
    """Vérifie une communication structurée belge."""
    s = normalize_ref(ref)
    if not (s.startswith("+++") and s.endswith("+++") and len(s) == 18):
        return False
    core = s[3:-3]
    if not (core.isdigit() and len(core) == 12):
        return False
    base, chk = int(core[:10]), int(core[10:])
    rem = base % 97
    if rem == 0:
        rem = 97
    return chk == rem

def iso11649_rf_check(ref: str) -> bool:
    """Vérifie une référence RF (ISO 11649)."""
    s = normalize_ref(ref)
    if not s.startswith("RF") or len(s) < 5:
        return False
    # Déplace 'RF' + 2 chiffres à la fin et convertit lettres -> nombres (A=10..Z=35)
    def to_num(c: str) -> str:
        return c if c.isdigit() else str(10 + ord(c) - ord("A"))
    rearranged = "".join(to_num(c) for c in (s[4:] + s[:4]))
    try:
        return int(rearranged) % 97 == 1
    except ValueError:
        return False

def epc_payload(
    creditor_name: str,
    iban: str,
    amount_eur: float,
    bic: str = "",
    purpose: str = "",
    reference: str = "",
    remittance: str = "",
) -> str:
    """
    Génère le payload texte pour QR EPC (SEPA Credit Transfer).
    À encoder en QR si besoin côté client.
    """
    name = (creditor_name or "")[:70]
    iban_clean = (iban or "").replace(" ", "").upper()
    lines = [
        "BCD",                # service tag
        "001",                # version
        "1",                  # charset (1 = UTF-8)
        "SCT",                # SEPA credit transfer
        (bic or "").upper(),
        name,
        iban_clean,
        f"EUR{float(amount_eur):.2f}",
        purpose or "",
        reference or "",
        remittance or "",
    ]
    return "\n".join(lines)

from uuid import uuid4

def make_token(sub: str, expires_in_seconds: int = 3600) -> str:
    """
    Génère un jeton 'fake' pour la beta (pas un JWT signé).
    Suffisant tant qu'on ne valide pas le token côté backend.
    """
    return f"stub.{uuid4().hex}"
