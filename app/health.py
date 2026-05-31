from sqlalchemy.orm import Session

from app.database import EventDB


def get_health(db: Session):

    total_events = db.query(EventDB).count()

    return {
        "status": "healthy",
        "database": "connected",
        "total_events": total_events
    }