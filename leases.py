from fastapi import APIRouter
router = APIRouter()

@router.get("")
def list_leases():
    return {"message": "list leases (stub)"}    

@router.post("")
def create_leases():
    return {"message": "create leases (stub)"}