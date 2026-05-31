# Engineering Choices and Trade-Offs

## Overview

This document explains the architectural and engineering decisions made while building the Store Intelligence System.

The challenge required balancing implementation complexity, development time, explainability, and production-readiness.

---

# 1. Event-Driven Architecture

## Choice

Use an event-driven system where all analytics are computed from events rather than directly from video streams.

## Why

Benefits:

* Decouples analytics from video processing
* Easier debugging and replayability
* Enables future streaming integrations
* Simplifies API implementation

## Trade-Off

Additional storage is required for event persistence.

Accepted because event storage is inexpensive and provides significant operational benefits.

---

# 2. FastAPI for Backend Services

## Choice

Use FastAPI as the backend framework.

## Why

* Automatic OpenAPI documentation
* Strong type validation via Pydantic
* High performance
* Easy integration with the Python AI ecosystem

## Alternatives Considered

### Flask

Pros:

* Simpler

Cons:

* Manual validation
* Manual API documentation

FastAPI was preferred due to built-in validation and documentation support.

---

# 3. SQLite for Persistence

## Choice

Use SQLite as the storage layer.

## Why

* Lightweight
* No infrastructure setup
* Fast local development
* Suitable for assessment-scale datasets

## Trade-Off

Not suitable for very large concurrent workloads.

### Production Upgrade Path

```text
SQLite
   ↓
PostgreSQL
```

The data-access layer was intentionally kept simple to support future migration.

---

# 4. YOLOv8 for Person Detection

## Choice

Use YOLOv8 for CCTV person detection.

## Why

* Excellent accuracy-to-speed ratio
* Easy deployment
* Strong community support
* Good performance on retail footage

## Alternatives Considered

### Faster R-CNN

Higher accuracy but slower inference.

### SSD

Faster but lower detection quality.

YOLOv8 provided the best balance between accuracy and inference speed.

---

# 5. ByteTrack for Tracking

## Choice

Use ByteTrack for multi-object tracking.

## Why

* Simple integration
* Good performance on crowded scenes
* Works directly with YOLO detections

## Observed Limitation

Identity switches may occur when:

* Visitors are partially occluded
* Visitors leave and re-enter view
* Multiple visitors move together

## Future Improvement

Introduce person re-identification models for cross-camera identity persistence.

---

# 6. First-Appearance Entry Logic

## Challenge

The provided CCTV footage did not always contain clearly visible physical store entry and exit events.

## Choice

Define:

```text
ENTRY = First appearance of visitor
EXIT  = Last observed appearance
```

## Why

Provides a practical approximation while remaining consistent across all footage.

## Trade-Off

May slightly overestimate visitor counts when tracking IDs change.

This limitation can be reduced using advanced tracking and re-identification techniques.

---

# 7. Zone Analytics

## Choice

Use zone-level events rather than frame-level analytics.

## Why

Business users care about:

* Which areas attract attention
* Dwell time
* Engagement

rather than individual frame detections.

This significantly reduces data volume and improves interpretability.

---

# 8. Heatmap Scoring

## Choice

Generate normalized heatmap scores.

Formula:

```text
Zone Visits / Maximum Zone Visits × 100
```

## Why

Allows easy comparison between zones regardless of store size.

Provides an intuitive measure of zone popularity.

---

# 9. Rule-Based Anomaly Detection

## Choice

Implement rule-based anomaly detection.

Examples:

* Conversion drops
* Queue spikes
* Dead zones

## Why

* Transparent logic
* Easy debugging
* Predictable outputs

## Future Improvement

Replace with machine-learning-based anomaly detection using historical store data.

---

# 10. Dockerized Deployment

## Choice

Containerize the entire backend.

## Why

* Consistent environment
* Easy evaluation
* Simplified deployment
* Reproducible builds

The application can be started using:

```bash
docker compose up --build
```

---

# Dataset Limitations

## Billing and Conversion Tracking

The provided dataset contains CCTV footage and store transaction records but does not provide a direct visitor-to-purchase mapping.

As a result:

```text
Visitor → Billing Event
```

cannot be reliably established for every individual visitor.

Therefore conversion rate is calculated conservatively and may remain zero when visitor-level billing linkage is unavailable.

The architecture fully supports conversion computation when billing events can be associated with tracked visitors.

---

# Known Limitations

1. Identity switching may occur during tracking.
2. Cross-camera visitor matching is not implemented.
3. Queue estimation currently uses event-based approximations.
4. Analytics are generated from processed footage rather than real-time streams.
5. Visitor-to-purchase attribution is limited by available dataset information.

---

# Future Roadmap

## Phase 1

* Multi-camera identity re-identification
* Improved visitor counting
* Product interaction detection

## Phase 2

* Kafka-based event streaming
* PostgreSQL migration
* Historical analytics warehouse

## Phase 3

* Real-time dashboard
* Forecasting models
* Staff optimization analytics
* Product-level conversion analytics

---

# Conclusion

The implemented solution prioritizes:

* Simplicity
* Reliability
* Explainability
* Extensibility

while maintaining a clear path toward production-scale deployment.

The architecture separates computer vision, event processing, storage, and analytics, enabling future expansion into real-time retail intelligence systems.
