from app.models import Event, Transaction, Merchant
from datetime import datetime

def ingest_event(db, event):

    existing = db.query(Event).filter_by(event_id=event.event_id).first()
    if existing:
        return "duplicate"

    
    db_event = Event(
    event_id=event.event_id,
    transaction_id=event.transaction_id,
    merchant_id=event.merchant_id,
    event_type=event.event_type,
    amount=event.amount,
    currency=event.currency,
    timestamp=event.timestamp
)
    db.add(db_event)

    merchant = db.query(Merchant).filter_by(merchant_id=event.merchant_id).first()
    if not merchant:
        merchant = Merchant(
            merchant_id=event.merchant_id,
            name=event.merchant_name
        )
        db.add(merchant)
    
    txn = db.query(Transaction).filter_by(transaction_id=event.transaction_id).first()

    if not txn:
        txn = Transaction(
            transaction_id=event.transaction_id,
            merchant_id=event.merchant_id,
            amount=event.amount,
            currency=event.currency,
            status="initiated",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(txn)

    if event.event_type == "payment_processed":
        if txn.status != "failed":
            txn.status = "processed"
    elif event.event_type == "payment_failed":
        txn.status = "failed"
    elif event.event_type == "settled":
        txn.status = "settled"

    txn.updated_at = datetime.utcnow()

    db.commit()
    return "processed"