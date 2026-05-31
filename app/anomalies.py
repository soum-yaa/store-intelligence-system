from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.database import EventDB


def get_anomalies(db: Session, store_id: str):

    anomalies = []

    queue_events = (
        db.query(EventDB)
        .filter(
            EventDB.store_id == store_id,
            EventDB.event_type == "BILLING_QUEUE_JOIN"
        )
        .all()
    )

    latest_queue_depth = 0

    for event in queue_events:
        if event.metadata_json:
            latest_queue_depth = max(
                latest_queue_depth,
                event.metadata_json.get("queue_depth") or 0
            )

    if latest_queue_depth >= 5:
        anomalies.append({
            "type": "BILLING_QUEUE_SPIKE",
            "severity": "WARN",
            "value": latest_queue_depth,
            "suggested_action": "Open an additional billing counter or assign staff to checkout."
        })

    total_entries = (
        db.query(EventDB)
        .filter(
            EventDB.store_id == store_id,
            EventDB.event_type == "ENTRY",
            EventDB.is_staff == False
        )
        .count()
    )

    billing_joins = (
        db.query(EventDB)
        .filter(
            EventDB.store_id == store_id,
            EventDB.event_type == "BILLING_QUEUE_JOIN",
            EventDB.is_staff == False
        )
        .count()
    )

    if total_entries >= 5 and billing_joins == 0:
        anomalies.append({
            "type": "CONVERSION_DROP",
            "severity": "WARN",
            "value": 0,
            "suggested_action": "Review product availability, staff assistance, and billing flow."
        })

    zone_visits = (
        db.query(EventDB)
        .filter(
            EventDB.store_id == store_id,
            EventDB.event_type == "ZONE_ENTER",
            EventDB.is_staff == False
        )
        .count()
    )

    if total_entries > 0 and zone_visits == 0:
        anomalies.append({
            "type": "DEAD_ZONE",
            "severity": "INFO",
            "value": zone_visits,
            "suggested_action": "Review zone visibility, placement, or camera coverage."
        })

    return {
        "store_id": store_id,
        "anomalies": anomalies
    }