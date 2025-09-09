# app/properties.py
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, HttpUrl

router = APIRouter()

# ----- Schéma de sortie -----
class PropertyOut(BaseModel):
    id: int
    title: str
    address: str
    city: Optional[str] = None
    rent: float
    currency: str = "EUR"
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    area_sqm: Optional[float] = None
    photo: Optional[HttpUrl] = None
    available: bool = True

# ----- “Mini base de données” en mémoire (démarrage rapide) -----
_DB: List[PropertyOut] = [
    PropertyOut(
        id=1,
        title="Studio lumineux centre-ville",
        address="12 Rue des Fleurs",
        city="Bruxelles",
        rent=650,
        currency="EUR",
        bedrooms=0,
        bathrooms=1,
        area_sqm=28,
        photo="https://picsum.photos/seed/memo1/800/600",
        available=True,
    ),
    PropertyOut(
        id=2,
        title="Appartement 1 ch. proche métro",
        address="89 Avenue Louise",
        city="Bruxelles",
        rent=980,
        currency="EUR",
        bedrooms=1,
        bathrooms=1,
        area_sqm=45,
        photo="https://picsum.photos/seed/memo2/800/600",
        available=True,
    ),
    PropertyOut(
        id=3,
        title="Duplex 2 ch. avec terrasse",
        address="5 Place des Arts",
        city="Liège",
        rent=1250,
        currency="EUR",
        bedrooms=2,
        bathrooms=1.5,
        area_sqm=82,
        photo="https://picsum.photos/seed/memo3/800/600",
        available=False,
    ),
]

# ----- Endpoints -----

@router.get("/", response_model=List[PropertyOut])
def list_properties(
    q: Optional[str] = Query(None, description="Recherche texte (titre / adresse)"),
    city: Optional[str] = Query(None),
    min_rent: Optional[float] = Query(None),
    max_rent: Optional[float] = Query(None),
    available: Optional[bool] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    items = _DB

    if q:
        ql = q.lower()
        items = [p for p in items if ql in p.title.lower() or ql in p.address.lower()]

    if city:
        items = [p for p in items if (p.city or "").lower() == city.lower()]

    if min_rent is not None:
        items = [p for p in items if p.rent >= min_rent]

    if max_rent is not None:
        items = [p for p in items if p.rent <= max_rent]

    if available is not None:
        items = [p for p in items if p.available == available]

    return items[offset : offset + limit]


@router.get("/{prop_id}", response_model=PropertyOut)
def get_property(prop_id: int):
    for p in _DB:
        if p.id == prop_id:
            return p
    raise HTTPException(status_code=404, detail="Property not found")
