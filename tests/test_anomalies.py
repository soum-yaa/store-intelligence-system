# PROMPT:
# Generate unit tests for anomaly detection in a retail store intelligence API.
# Cover conversion drop and billing queue spike scenarios.
#
# CHANGES MADE:
# Adapted tests to the current rule-based anomaly implementation.
# Used isolated in-memory SQLite setup to avoid depending on production store.db.

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, EventDB
from app.anomalies import get_anomalies


def create_test_db():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()


def test_conversion_drop_detected_when_entries_exist_without_billing():
    db = create_test_db()

    for i in range(5):
        db.add(
            EventDB(
                event_id=f"entry_{i}",
                store_id="STORE_TEST",
                camera_id="CAM_1",
                visitor_id=f"VIS_{i}",
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

    result = get_anomalies(db, "STORE_TEST")

    anomaly_types = [a["type"] for a in result["anomalies"]]

    assert "CONVERSION_DROP" in anomaly_types


def test_billing_queue_spike_detected():
    db = create_test_db()

    db.add(
        EventDB(
            event_id="queue_1",
            store_id="STORE_TEST",
            camera_id="CAM_BILLING",
            visitor_id="VIS_1",
            event_type="BILLING_QUEUE_JOIN",
            timestamp=datetime.utcnow(),
            zone_id="BILLING",
            dwell_ms=0,
            is_staff=False,
            confidence=0.9,
            metadata_json={"queue_depth": 6, "session_seq": 2}
        )
    )

    db.commit()

    result = get_anomalies(db, "STORE_TEST")

    anomaly_types = [a["type"] for a in result["anomalies"]]

    assert "BILLING_QUEUE_SPIKE" in anomaly_types