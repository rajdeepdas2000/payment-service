from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Transaction, Event, Merchant
from app.deps import get_db
from datetime import datetime

router = APIRouter()

@router.get("/transactions")
def list_transactions(
    merchant_id: str = None,
    status: str = None,
    start_date: datetime = None, 
    end_date: datetime = None,     
    sort_by: str = "created_at",   
    order: str = "desc",           
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)

    if merchant_id:
        query = query.filter(Transaction.merchant_id == merchant_id)

    if status:
        query = query.filter(Transaction.status == status)

    if start_date:
        query = query.filter(Transaction.created_at >= start_date)

    if end_date:
        query = query.filter(Transaction.created_at <= end_date)

    sort_column = getattr(Transaction, sort_by, Transaction.created_at)

    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    return query.offset(skip).limit(limit).all()


@router.get("/transactions/{txn_id}")
def get_transaction(txn_id: str, db: Session = Depends(get_db)):
    txn = db.query(Transaction).filter_by(transaction_id=txn_id).first()

    if not txn:
        return {"error": "transaction not found"}

    events = db.query(Event).filter_by(transaction_id=txn_id).all()

    merchant = db.query(Merchant).filter_by(
        merchant_id=txn.merchant_id
    ).first()

    return {
        "transaction": txn,
        "merchant": merchant,
        "events": events
    }