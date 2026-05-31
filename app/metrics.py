from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import EventDB


def get_store_metrics(db: Session, store_id: str):

    customer_events = db.query(EventDB).filter(
        EventDB.store_id == store_id,
        EventDB.is_staff == False
    )

    total_events = customer_events.count()

    unique_visitors = (
        customer_events
        .with_entities(EventDB.visitor_id)
        .distinct()
        .count()
    )

    entries = customer_events.filter(EventDB.event_type == "ENTRY").count()
    exits = customer_events.filter(EventDB.event_type == "EXIT").count()

    billing_queue_joins = customer_events.filter(
        EventDB.event_type == "BILLING_QUEUE_JOIN"
    ).count()

    abandonments = customer_events.filter(
        EventDB.event_type == "BILLING_QUEUE_ABANDON"
    ).count()

    conversion_rate = 0
    if unique_visitors > 0:
        conversion_rate = round((billing_queue_joins / unique_visitors) * 100, 2)

    abandonment_rate = 0
    if billing_queue_joins > 0:
        abandonment_rate = round((abandonments / billing_queue_joins) * 100, 2)

    avg_dwell_rows = (
        db.query(
            EventDB.zone_id,
            func.avg(EventDB.dwell_ms).label("avg_dwell_ms")
        )
        .filter(
            EventDB.store_id == store_id,
            EventDB.is_staff == False,
            EventDB.event_type == "ZONE_DWELL",
            EventDB.zone_id.isnot(None)
        )
        .group_by(EventDB.zone_id)
        .all()
    )

    avg_dwell_per_zone = {}

    for zone_id, avg_dwell_ms in avg_dwell_rows:
        avg_dwell_per_zone[zone_id] = round(avg_dwell_ms, 2)

    latest_queue_event = (
        db.query(EventDB)
        .filter(
            EventDB.store_id == store_id,
            EventDB.event_type == "BILLING_QUEUE_JOIN"
        )
        .order_by(EventDB.timestamp.desc())
        .first()
    )

    queue_depth = 0

    if latest_queue_event and latest_queue_event.metadata_json:
        queue_depth = latest_queue_event.metadata_json.get("queue_depth") or 0

    return {
        "store_id": store_id,
        "total_events": total_events,
        "unique_visitors": unique_visitors,
        "entries": entries,
        "exits": exits,
        "conversion_rate": conversion_rate,
        "avg_dwell_per_zone": avg_dwell_per_zone,
        "queue_depth": queue_depth,
        "abandonment_rate": abandonment_rate
    }