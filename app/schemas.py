from pydantic import BaseModel
from datetime import datetime

class EventSchema(BaseModel):
    event_id: str
    event_type: str
    transaction_id: str
    merchant_id: str
    merchant_name: str
    amount: float
    currency: str
    timestamp: datetime