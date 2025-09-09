from typing import List
from fastapi import APIRouter
from pydantic import BaseModel, AnyUrl

router = APIRouter()

class Document(BaseModel):
    id: int
    name: str
    url: AnyUrl

_DOCS: List[Document] = [
    Document(id=1, name="Etat des lieux.pdf", url="https://example.com/doc1.pdf")
]

@router.get("")
def list_documents():
    return {"items": [d.model_dump() for d in _DOCS], "count": len(_DOCS)}

@router.post("")
def create_document(doc: Document):
    _DOCS.append(doc)
    return {"created": doc.model_dump()}
