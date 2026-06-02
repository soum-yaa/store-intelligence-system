# PROMPT:
# Generate unit tests for the store metrics calculation logic in a FastAPI retail analytics project.
# Test unique visitors, entries, exits, dwell time, queue depth, and staff exclusion.
#
# CHANGES MADE:
# Adapted the tests to use an isolated in-memory SQLite database and the actual EventDB model.
# Added staff-exclusion verification and dwell-time aggregation checks.

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, EventDB
from app.metrics import get_store_metrics


def create_test_db():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()


def test_metrics_excludes_staff_and_computes_counts():
    db = create_test_db()

    db.add_all([
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
        ),
        EventDB(
            event_id="e2",
            store_id="STORE_TEST",
            camera_id="CAM_1",
            visitor_id="VIS_1",
            event_type="EXIT",
            timestamp=datetime.utcnow(),
            zone_id=None,
            dwell_ms=0,
            is_staff=False,
            confidence=0.9,
            metadata_json={"queue_depth": None, "session_seq": 2}
        ),
        EventDB(
            event_id="e3",
            store_id="STORE_TEST",
            camera_id="CAM_1",
            visitor_id="STAFF_1",
            event_type="ENTRY",
            timestamp=datetime.utcnow(),
            zone_id=None,
            dwell_ms=0,
            is_staff=True,
            confidence=0.9,
            metadata_json={"queue_depth": None, "session_seq": 1}
        ),
    ])

    db.commit()

    result = get_store_metrics(db, "STORE_TEST")

    assert result["total_events"] == 2
    assert result["unique_visitors"] == 1
    assert result["entries"] == 1
    assert result["exits"] == 1


def test_metrics_computes_avg_dwell_and_queue_depth():
    db = create_test_db()

    db.add_all([
        EventDB(
            event_id="e1",
            store_id="STORE_TEST",
            camera_id="CAM_1",
            visitor_id="VIS_1",
            event_type="ZONE_DWELL",
            timestamp=datetime.utcnow(),
            zone_id="MAIN_ZONE",
            dwell_ms=30000,
            is_staff=False,
            confidence=0.9,
            metadata_json={"queue_depth": None, "session_seq": 1}
        ),
        EventDB(
            event_id="e2",
            store_id="STORE_TEST",
            camera_id="CAM_1",
            visitor_id="VIS_2",
            event_type="ZONE_DWELL",
            timestamp=datetime.utcnow(),
            zone_id="MAIN_ZONE",
            dwell_ms=60000,
            is_staff=False,
            confidence=0.9,
            metadata_json={"queue_depth": None, "session_seq": 1}
        ),
        EventDB(
            event_id="e3",
            store_id="STORE_TEST",
            camera_id="CAM_BILLING",
            visitor_id="VIS_2",
            event_type="BILLING_QUEUE_JOIN",
            timestamp=datetime.utcnow(),
            zone_id="BILLING",
            dwell_ms=0,
            is_staff=False,
            confidence=0.9,
            metadata_json={"queue_depth": 4, "session_seq": 2}
        ),
    ])

    db.commit()

    result = get_store_metrics(db, "STORE_TEST")

    assert result["avg_dwell_per_zone"]["MAIN_ZONE"] == 45000
    assert result["queue_depth"] == 4