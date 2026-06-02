from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import EventDB
from app.models import Event


def save_event(db: Session, event: Event):

    db_event = EventDB(
        event_id=event.event_id,
        store_id=event.store_id,
        camera_id=event.camera_id,
        visitor_id=event.visitor_id,
        event_type=event.event_type,
        timestamp=event.timestamp,
        zone_id=event.zone_id,
        dwell_ms=event.dwell_ms,
        is_staff=event.is_staff,
        confidence=event.confidence,
        metadata_json=(
            event.metadata.model_dump()
            if event.metadata
            else None
        )
    )

    try:
        db.add(db_event)
        db.commit()
        return True

    except IntegrityError:
        db.rollback()
        return False