from fastapi import FastAPI
from app.database import Base, engine
from routes import events, transactions, reconciliation

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Payment Reconciliation Service")

app.include_router(events.router)
app.include_router(transactions.router)
app.include_router(reconciliation.router)