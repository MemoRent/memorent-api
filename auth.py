# auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import make_token

router = APIRouter()

class LoginIn(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(body: LoginIn):
    # Bêta : on accepte les identifiants sans vérifier en base
    if not body.email or not body.password:
        raise HTTPException(status_code=400, detail="email and password required")

    token = make_token(body.email)  # utilises ta fonction utilitaire
    return {"access_token": token, "token_type": "bearer"}
