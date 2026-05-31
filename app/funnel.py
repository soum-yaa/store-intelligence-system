from sqlalchemy.orm import Session

from app.database import EventDB


def get_funnel(db: Session, store_id: str):

    entries = (
        db.query(EventDB)
        .filter(
            EventDB.store_id == store_id,
            EventDB.event_type == "ENTRY"
        )
        .count()
    )

    zone_enters = (
        db.query(EventDB)
        .filter(
            EventDB.store_id == store_id,
            EventDB.event_type == "ZONE_ENTER"
        )
        .count()
    )

    billing_queue = (
        db.query(EventDB)
        .filter(
            EventDB.store_id == store_id,
            EventDB.event_type == "BILLING_QUEUE_JOIN"
        )
        .count()
    )

    exits = (
        db.query(EventDB)
        .filter(
            EventDB.store_id == store_id,
            EventDB.event_type == "EXIT"
        )
        .count()
    )

    conversion_rate = 0

    if entries > 0:
        conversion_rate = round(
            (billing_queue / entries) * 100,
            2
        )

    return {
        "store_id": store_id,
        "entries": entries,
        "zone_enters": zone_enters,
        "billing_queue": billing_queue,
        "exits": exits,
        "conversion_rate": conversion_rate
    }