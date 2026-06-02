# PROMPT:
# Generate unit tests for a FastAPI service health function that checks database connectivity
# and returns stored event counts.
#
# CHANGES MADE:
# Adapted the test to call the actual get_health function using an isolated SQLite database.

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, EventDB
from app.health import get_health


def create_test_db():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()


def test_health_returns_status_and_total_events():
    db = create_test_db()

    db.add(
        EventDB(
            event_id="e1",
            store_id="STORE_TEST",
            camera_id="CAM_1",
            visitor_id="VIS_1",
            event_type="ENTRY",
            timestamp=datetime.utcnow(),
            zone_id=None,
            dwell_ms=0,
            is_staff=False,
            confidence=0.9,
            metadata_json={"queue_depth": None, "session_seq": 1}
        )
    )

    db.commit()

    result = get_health(db)

    assert result["status"] == "healthy"
    assert result["database"] == "connected"
    assert result["total_events"] == 1