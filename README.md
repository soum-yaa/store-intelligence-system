# Store Intelligence Backend

## Overview

Store Intelligence Backend is a FastAPI-based analytics platform for processing retail store events and generating actionable business insights.

The system supports:

* Event ingestion
* Store metrics computation
* Funnel analytics
* Heatmap analytics
* Anomaly detection
* Health monitoring
* Docker deployment

The project also includes a computer vision pipeline that processes CCTV footage, tracks visitors, and generates structured store events.

---

## Architecture

```text
CCTV Videos
      |
      v
YOLOv8 Detection
      |
      v
Multi-Object Tracking
      |
      v
Event Generation
      |
      v
FastAPI Ingestion API
      |
      v
SQLite Database
      |
      +--------------------+
      |                    |
      v                    v
Analytics APIs      Monitoring APIs
```

---

## Architecture Diagram

The complete system architecture is available in:

```text
docs/architecture.png
```

---

## Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* SQLite
* Pydantic

### Computer Vision

* YOLOv8
* OpenCV
* Supervision

### Deployment

* Docker
* Docker Compose

---

## Project Structure

```text
project/
│
├── app/
│   ├── main.py
│   ├── ingestion.py
│   ├── metrics.py
│   ├── funnel.py
│   ├── heatmap.py
│   ├── anomalies.py
│   ├── health.py
│   ├── database.py
│   └── models.py
│
├── pipeline/
│   ├── detect.py
│   ├── detect_visual.py
│   ├── track_cam3.py
│   ├── generate_events_cam1.py
│   └── push_events.py
│
├── output/
│
├── docs/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Running Locally

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start API

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Running With Docker

Build and start:

```bash
docker compose up --build
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Running the Detection Pipeline

The detection pipeline converts CCTV footage into structured behavioural events.

### 1. Run Person Detection

```bash
python pipeline/detect.py
```

### 2. Generate Detection Video with Bounding Boxes

```bash
python pipeline/detect_visual.py
```

### 3. Run Tracking

```bash
python pipeline/track_cam3.py
```

### 4. Generate Events from CCTV

```bash
python pipeline/generate_events_cam1.py
```

Generated events are saved at:

```text
output/events.jsonl
```

### 5. Push Generated Events to API

First start the API:

```bash
docker compose up --build
```

Then in another terminal run:

```bash
python pipeline/push_events.py
```

This sends events from:

```text
output/events.jsonl
```

to:

```text
POST /events/ingest
```

---

## API Endpoints

### Health

```text
GET /health
```

Returns service health status and database connectivity.

---

### Event Ingestion

```text
POST /events/ingest
```

Stores incoming store events.

---

### Metrics

```text
GET /stores/{store_id}/metrics
```

Returns:

* Total events
* Unique visitors
* Entries
* Exits
* Conversion rate
* Queue depth
* Average dwell time
* Abandonment rate

---

### Funnel Analytics

```text
GET /stores/{store_id}/funnel
```

Returns visitor funnel metrics.

---

### Heatmap Analytics

```text
GET /stores/{store_id}/heatmap
```

Returns zone popularity information.

---

### Anomaly Detection

```text
GET /stores/{store_id}/anomalies
```

Returns operational anomalies.

---

## Sample Results

Processed Store:

```text
STORE_001
```

Generated Analytics:

* Total Events: 64
* Unique Visitors: 20
* Entries: 20
* Exits: 18
* Heatmap Analytics across multiple store zones
* Automatic anomaly detection
* Visitor dwell-time computation

---

## Assessment Deliverables

This submission includes:

* FastAPI backend services
* Event ingestion pipeline
* Store analytics APIs
* Funnel analytics
* Heatmap analytics
* Anomaly detection
* Health monitoring APIs
* SQLite persistence layer
* Dockerized deployment
* Computer vision event generation pipeline
* System design documentation
* Architecture diagram

---

## Future Improvements

* Multi-camera identity matching
* Queue estimation
* Real-time event streaming
* Interactive dashboard
* Advanced conversion analytics
* Product-level shopper journey analysis

---

## Author

Soumya Verma

B.Tech Final Year

Madan Mohan Malaviya University of Technology

Store Intelligence Assessment Submission
