import time
import uuid
import logging
from typing import List

from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session

from app.models import Event
from app.database import SessionLocal
from app.ingestion import save_event
from app.metrics import get_store_metrics
from app.health import get_health
from app.funnel import get_funnel
from app.heatmap import get_heatmap
from app.anomalies import get_anomalies


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

logger = logging.getLogger("store-intelligence-api")


app = FastAPI(
    title="Store Intelligence API"
)


@app.middleware("http")
async def structured_logging_middleware(request: Request, call_next):
    trace_id = str(uuid.uuid4())
    start_time = time.time()

    response = await call_next(request)

    latency_ms = round((time.time() - start_time) * 1000, 2)

    endpoint = request.url.path
    store_id = request.path_params.get("store_id", None)

    log_payload = {
        "trace_id": trace_id,
        "endpoint": endpoint,
        "store_id": store_id,
        "latency_ms": latency_ms,
        "status_code": response.status_code
    }

    logger.info(log_payload)

    response.headers["X-Trace-Id"] = trace_id

    return response


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "Store Intelligence API Running"
    }


@app.post("/events/ingest")
def ingest_events(
    events: List[Event],
    db: Session = Depends(get_db)
):
    stored = 0
    duplicates = 0

    for event in events:
        success = save_event(db, event)

        if success:
            stored += 1
        else:
            duplicates += 1

    return {
        "message": "Batch processed",
        "received": len(events),
        "stored": stored,
        "duplicates": duplicates
    }


@app.get("/stores/{store_id}/metrics")
def store_metrics(
    store_id: str,
    db: Session = Depends(get_db)
):
    return get_store_metrics(db, store_id)


@app.get("/stores/{store_id}/funnel")
def store_funnel(
    store_id: str,
    db: Session = Depends(get_db)
):
    return get_funnel(db, store_id)


@app.get("/stores/{store_id}/heatmap")
def store_heatmap(
    store_id: str,
    db: Session = Depends(get_db)
):
    return get_heatmap(db, store_id)


@app.get("/stores/{store_id}/anomalies")
def store_anomalies(
    store_id: str,
    db: Session = Depends(get_db)
):
    return get_anomalies(db, store_id)


@app.get("/health")
def health(
    db: Session = Depends(get_db)
):
    return get_health(db)