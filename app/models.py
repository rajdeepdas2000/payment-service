from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Index
from app.database import Base

class Merchant(Base):
    __tablename__ = "merchants"
    merchant_id = Column(String, primary_key=True)
    name = Column(String)

class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(String, primary_key=True)
    merchant_id = Column(String, ForeignKey("merchants.merchant_id"))
    amount = Column(Float)
    currency = Column(String)
    status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Event(Base):
    __tablename__ = "events"
    event_id = Column(String, primary_key=True)
    transaction_id = Column(String)
    merchant_id = Column(String)
    event_type = Column(String)
    amount = Column(Float)
    currency = Column(String)
    timestamp = Column(DateTime)

Index("idx_txn_merchant", Transaction.merchant_id)
Index("idx_txn_status", Transaction.status)
Index("idx_events_txn", Event.transaction_id)