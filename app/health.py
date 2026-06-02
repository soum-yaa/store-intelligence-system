from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database import EventDB


def get_health(db: Session):

    total_events = db.query(EventDB).count()

    latest_event = (
        db.query(EventDB)
        .order_by(EventDB.timestamp.desc())
        .first()
    )

    last_event_timestamp = None
    stale_feed = False

    if latest_event:
        last_event_timestamp = latest_event.timestamp.isoformat()

        now = datetime.now(timezone.utc)

        event_time = latest_event.timestamp

        if event_time.tzinfo is None:
            event_time = event_time.replace(tzinfo=timezone.utc)

        minutes_since_last_event = (
            now - event_time
        ).total_seconds() / 60

        stale_feed = minutes_since_last_event > 30

    return {
        "status": "healthy",
        "database": "connected",
        "total_events": total_events,
        "last_event_timestamp": last_event_timestamp,
        "stale_feed": stale_feed
    }