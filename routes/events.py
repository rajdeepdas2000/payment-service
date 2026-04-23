from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import EventSchema
from app.deps import get_db
from app.crud import ingest_event

router = APIRouter()

@router.post("/events")
def create_event(event: EventSchema, db: Session = Depends(get_db)):
    result = ingest_event(db, event)
    return {"status": result,
            "event_id": event.event_id,
            "transaction_id": event.transaction_id}