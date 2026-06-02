# System Design

## Objective

The goal of the system is to transform raw retail store events into actionable business insights.

The platform ingests events generated from store operations or computer vision pipelines and provides analytics APIs for monitoring visitor behavior, store performance, and operational anomalies.

---

# High-Level Architecture

```text
CCTV Footage
      |
      v
YOLOv8 Person Detection
      |
      v
Object Tracking
      |
      v
Event Generation
      |
      v
Event Ingestion API
      |
      v
SQLite Database
      |
      +---------------------+
      |                     |
      v                     v
Analytics Engine     Monitoring Engine
      |
      v
REST API Responses
```

---

# Processing Pipeline

```text
CAM1 / CAM2 / CAM3 CCTV Videos
              |
              v
        YOLOv8 Detection
              |
              v
       ByteTrack Tracking
              |
              v
     Event Generation (.jsonl)
              |
              v
      FastAPI Batch Ingestion
              |
              v
         SQLite Database
              |
     +--------+--------+--------+
     |        |        |        |
     v        v        v        v
 Metrics   Funnel   Heatmap  Anomalies
              |
              v
          REST APIs
```

This pipeline represents the complete flow from raw CCTV footage to business intelligence APIs.


# Components

## 1. Computer Vision Pipeline

The computer vision pipeline processes CCTV footage and generates structured events.

### Responsibilities

* Detect people using YOLOv8
* Track people across frames
* Generate visitor events
* Export events in JSONL format

### Output Example

```json
{
  "event_id": "evt_001",
  "visitor_id": "VIS_001",
  "event_type": "ENTRY",
  "store_id": "STORE_001"
}
```

---

## 2. Event Ingestion Service

The ingestion service exposes an API endpoint for receiving events.

### Endpoint

```text
POST /events/ingest
```

### Responsibilities

* Validate event schema
* Prevent duplicate event insertion
* Store events in database
* Return ingestion status

---

## 3. Storage Layer

SQLite is used as the persistence layer.

### Event Schema

| Field      | Description             |
| ---------- | ----------------------- |
| event_id   | Unique event identifier |
| store_id   | Store identifier        |
| visitor_id | Visitor identifier      |
| event_type | Type of event           |
| zone_id    | Zone identifier         |
| dwell_ms   | Time spent in zone      |
| is_staff   | Staff flag              |
| confidence | Detection confidence    |

---

## 4. Metrics Engine

The metrics engine computes store-level KPIs.

### Supported Metrics

* Total Events
* Unique Visitors
* Entries
* Exits
* Conversion Rate
* Average Dwell Time
* Queue Depth
* Abandonment Rate

### Endpoint

```text
GET /stores/{store_id}/metrics
```

---

## 5. Funnel Analytics Engine

Tracks visitor progression through the store.

### Stages

```text
ENTRY
  ↓
ZONE_VISIT
  ↓
BILLING
  ↓
EXIT
```

### Endpoint

```text
GET /stores/{store_id}/funnel
```

---

## 6. Heatmap Analytics Engine

Provides zone popularity information.

### Metrics

* Number of visits
* Average dwell time
* Heatmap score

### Endpoint

```text
GET /stores/{store_id}/heatmap
```

---

## 7. Anomaly Detection Engine

Detects operational issues.

### Examples

* Conversion drops
* Excessive queue depth
* Low engagement zones

### Endpoint

```text
GET /stores/{store_id}/anomalies
```

---

## 8. Health Monitoring

Provides application health information.

### Endpoint

```text
GET /health
```

### Returned Information

* Service status
* Database connectivity
* Total stored events

---

# Deployment Design

The application is containerized using Docker.

### Components

```text
Docker Container
    |
    +-- FastAPI
    +-- SQLite
    +-- Analytics Services
```

Docker Compose is used for local deployment and testing.

---

# Design Decisions

### Why FastAPI?

* High performance
* Automatic OpenAPI documentation
* Easy schema validation

### Why SQLite?

* Lightweight
* Zero configuration
* Suitable for assessment-scale workloads

### Why YOLOv8?

* Fast inference
* Strong person detection performance
* Easy integration with OpenCV

### Why Event-Driven Design?

* Decouples ingestion from analytics
* Easier future scalability
* Supports real-time streaming extensions

---

# AI-Assisted Decisions

## 1. Detection Model Selection

AI assistance was used to compare multiple person-detection approaches such as YOLOv8, RT-DETR, MediaPipe, and heavier two-stage detectors.

The AI suggestion was to begin with YOLOv8 because it provides a strong balance between detection quality, inference speed, ease of integration, and deployment simplicity.

I agreed with this recommendation and selected YOLOv8 because the challenge focuses on building a complete end-to-end system rather than training a custom model from scratch. YOLOv8 also integrates easily with OpenCV and supports fast experimentation on retail CCTV footage.

## 2. Tracking and Visitor Identity

AI suggested using a tracking layer after detection instead of counting raw detections frame by frame.

I followed this suggestion and used ByteTrack-style tracking because counting detections directly would overcount the same visitor across frames. Tracking allows the system to assign visitor IDs and generate higher-level events such as ENTRY, EXIT, ZONE_DWELL, and REENTRY.

During testing, I observed that identity switches can still occur during occlusion or when people move together. This limitation is documented in CHOICES.md, and the future improvement path is to add stronger person re-identification.

## 3. Event Schema Design

AI initially suggested a minimal schema containing visitor ID, event type, timestamp, and store ID.

I expanded the schema to include camera_id, zone_id, dwell_ms, is_staff, confidence, and metadata because these fields are required for downstream analytics such as heatmap generation, funnel computation, staff exclusion, queue tracking, and anomaly detection.

This decision made the event layer more expressive and closer to production use.

## 4. API Architecture

AI suggested two approaches for analytics computation:

1. Precompute metrics during ingestion.
2. Compute metrics at query time from the event table.

I chose query-time computation for this assessment because it keeps the implementation simple, transparent, and easy to debug. It also ensures that API responses always reflect the latest stored events.

For a larger production system, the design can evolve toward pre-aggregated metrics using a streaming system such as Kafka or Redis streams.

## 5. Documentation and Trade-Off Review

AI was also used to review implementation trade-offs and identify missing evaluation criteria such as Docker execution, documentation, idempotent ingestion, and explainable anomaly detection.

I used these suggestions as a checklist, but retained the final decisions based on project constraints, implementation time, and the scoring rubric.

# Future Enhancements

## Computer Vision

* Multi-camera visitor re-identification
* Improved identity persistence
* Product interaction detection
* Shelf engagement analytics

## Data Platform

* Kafka-based event streaming
* PostgreSQL migration
* Historical analytics warehouse

## Analytics

* Real-time dashboard
* Staff optimization recommendations
* Queue forecasting
* Conversion prediction models
* Product-level conversion analytics

## Deployment

* Kubernetes deployment
* Cloud-native monitoring
* Horizontal scaling support

