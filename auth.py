from fastapi import APIRouter
router = APIRouter()

@router.post("/register")
def register():
    return {"message": "register (stub)"}

@router.post("/login")
def login():
    return {"access_token": "stub", "token_type": "bearer"}