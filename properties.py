from fastapi import APIRouter
router = APIRouter()

@router.get("")
def list_properties():
    return {"message": "list properties (stub)"}    

@router.post("")
def create_properties():
    return {"message": "create properties (stub)"}