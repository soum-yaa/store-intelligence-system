from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import EventDB


def get_heatmap(db: Session, store_id: str):

    rows = (
        db.query(
            EventDB.zone_id,
            func.count().label("visits"),
            func.avg(EventDB.dwell_ms).label("avg_dwell_ms")
        )
        .filter(
            EventDB.store_id == store_id,
            EventDB.is_staff == False,
            EventDB.zone_id.isnot(None)
        )
        .group_by(EventDB.zone_id)
        .all()
    )

    total_sessions = (
        db.query(EventDB.visitor_id)
        .filter(
            EventDB.store_id == store_id,
            EventDB.is_staff == False,
            EventDB.event_type == "ENTRY"
        )
        .distinct()
        .count()
    )

    max_visits = max([row.visits for row in rows], default=1)

    zones = []

    for row in rows:
        zones.append({
            "zone_id": row.zone_id,
            "visits": row.visits,
            "avg_dwell_ms": round(row.avg_dwell_ms or 0, 2),
            "heatmap_score": round((row.visits / max_visits) * 100, 2)
        })

    return {
        "store_id": store_id,
        "data_confidence": "LOW" if total_sessions < 20 else "HIGH",
        "total_sessions": total_sessions,
        "zones": zones
    }