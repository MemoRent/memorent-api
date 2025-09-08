from fastapi import APIRouter
router = APIRouter()

@router.get("")
def list_documents():
    return {"documents": []}

@router.post("")
def create_document():
    # In real life: return pre-signed URL for upload to S3/Wasabi/etc.
    return {"upload_url": "https://storage.example/presigned", "id": 1}