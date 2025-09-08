from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Imports des routers (fichiers .py à la racine du repo)
from auth import router as auth_router
from properties import router as properties_router
from leases import router as leases_router
from payments import router as payments_router
from tickets import router as tickets_router
from documents import router as documents_router
from dashboard import router as dashboard_router
from webhooks import router as webhooks_router
from invoices import router as invoices_router
from reminders import router as reminders_router

app = FastAPI(title="MemoRent API (MVP)")

# CORS large pour le MVP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Déclaration des routes (une ligne par router)
app.include_router(auth_router,       prefix="/auth",       tags=["auth"])
app.include_router(properties_router, prefix="/properties", tags=["properties"])
app.include_router(leases_router,     prefix="/leases",     tags=["leases"])
app.include_router(payments_router,   prefix="/payments",   tags=["payments"])
app.include_router(tickets_router,    prefix="/tickets",    tags=["tickets"])
app.include_router(documents_router,  prefix="/documents",  tags=["documents"])
app.include_router(dashboard_router,  prefix="/dashboard",  tags=["dashboard"])
app.include_router(webhooks_router,   prefix="/webhooks",   tags=["webhooks"])
app.include_router(invoices_router,   prefix="/invoices",   tags=["invoices"])
app.include_router(reminders_router,  prefix="/reminders",  tags=["reminders"])

@app.get("/health")
def health():
    return {"status": "ok"}
