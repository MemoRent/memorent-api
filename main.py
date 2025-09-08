from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, properties, leases, tickets, documents, payments, dashboard, webhooks, invoices, reminders

app = FastAPI(title="LocA - Gestion Locative Belgique (MVP)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(properties.router, prefix="/properties", tags=["properties"])
app.include_router(leases.router, prefix="/leases", tags=["leases"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])\napp.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])\napp.include_router(invoices.router, prefix="/invoices", tags=["invoices"])\napp.include_router(reminders.router, prefix="/reminders", tags=["reminders"])

@app.get("/health")
def health():
    return {"status": "ok"}