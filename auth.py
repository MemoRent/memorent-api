# auth.py
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from utils import make_token

# mini-bases en mémoire importées depuis les modules
from properties import _DB as _PROPERTIES
from leases import _LEASES
from invoices import _INVOICES
from tickets import _TICKETS
from documents import _DOCS
from dashboard import summary as dashboard_summary  # on appelle directement la fonction

router = APIRouter()

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str  # "tenant" | "owner"

_USERS = [
    User(id=1, name="Alice Propriétaire", email="owner@memorent.app", role="owner"),
    User(id=2, name="Bob Locataire",    email="tenant@memorent.app", role="tenant"),
]

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User
    bootstrap: Dict[str, Any]

@router.post("/login", response_model=LoginOut)
def login(payload: LoginIn):
    # MVP: on vérifie seulement l'email présent dans la mini-base
    user: Optional[User] = next((u for u in _USERS if u.email == payload.email), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = make_token(user.email)

    # appelle direct la fonction summary() du dashboard
    dash = dashboard_summary()

    bootstrap = {
        "properties": [p.dict() for p in _PROPERTIES],
        "leases":     [l.dict() for l in _LEASES],
        "invoices":   [i.dict() for i in _INVOICES],
        "tickets":    [t.dict() for t in _TICKETS],
        "documents":  [d.dict() for d in _DOCS],
        "dashboard":  {"summary": dash},
    }
    return LoginOut(access_token=token, user=user, bootstrap=bootstrap)
