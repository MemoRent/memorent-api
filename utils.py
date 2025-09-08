import re

def normalize_ref(s: str) -> str:
    return s.upper().replace(' ', '').replace('/', '')

def be_structured_build(core10: str) -> str:
    assert core10.isdigit() and len(core10) == 10
    rem = int(core10) % 97
    if rem == 0:
        rem = 97
    return f"+++{core10}{rem:02d}+++"

def be_structured_check(ref: str) -> bool:
    s = normalize_ref(ref)
    if not (s.startswith('+++') and s.endswith('+++') and len(s) == 18):
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
    s = normalize_ref(ref)
    if not s.startswith('RF') or len(s) < 5:
        return False
    # Move 'RF' and two check digits to end and convert letters -> numbers (A=10..Z=35)
    def to_num(c):
        if c.isdigit():
            return c
        return str(ord(c) - 55)  # A=10
    rearranged = ''.join(to_num(c) for c in s[4:] + s[:4])
    return int(rearranged) % 97 == 1

def epc_payload(creditor_name: str, iban: str, amount_eur: float,
                bic: str = '', purpose: str = '', reference: str = '', remittance: str = '') -> str:
    lines = [
        'BCD',      # service tag
        '001',      # version
        '1',        # character set (1=UTF-8)
        'SCT',      # SEPA credit transfer
        bic or '',
        creditor_name[:70],
        iban.replace(' ', ''),
        f"EUR{amount_eur:.2f}",
        purpose or '',
        reference or '',
        remittance or '',
    ]
    return '\n'.join(lines)