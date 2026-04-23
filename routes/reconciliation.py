from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from app.models import Transaction, Event
from app.deps import get_db

router = APIRouter()

@router.get("/reconciliation/summary")
def summary(db: Session = Depends(get_db)):
    result = db.query(
        Transaction.merchant_id,
        func.date(Transaction.created_at).label("date"),
        Transaction.status,
        func.count().label("count")
    ).group_by(
        Transaction.merchant_id,
        func.date(Transaction.created_at),
        Transaction.status
    ).all()

    return [
    {
        "merchant_id": r[0],
        "date": str(r[1]),
        "status": r[2],
        "count": r[3]
    }
    for r in result
]


@router.get("/reconciliation/discrepancies")
def discrepancies(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT * FROM transactions t
        WHERE 
            (status = 'processed' AND NOT EXISTS (
                SELECT 1 FROM events e 
                WHERE e.transaction_id = t.transaction_id 
                AND e.event_type = 'settled'
            ))
            OR
            (status = 'failed' AND EXISTS (
                SELECT 1 FROM events e 
                WHERE e.transaction_id = t.transaction_id 
                AND e.event_type = 'settled'
            ))
    """))
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]