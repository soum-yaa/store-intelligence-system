# Store Intelligence Backend

## Overview

Store Intelligence Backend is a FastAPI-based analytics platform for processing retail store events and generating operational insights.

The system supports:

* Event ingestion
* Store metrics computation
* Funnel analytics
* Heatmap analytics
* Anomaly detection
* Health monitoring
* Docker deployment

The project also includes a computer vision pipeline that processes CCTV footage, tracks visitors, and generates store events.

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

See:

docs/architecture.png

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
│   ├── track_cam3.py
│   ├── generate_events.py
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

Windows:

```bash
venv\Scripts\activate
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

## API Endpoints

### Health

```text
GET /health
```

Returns service health status.

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

* total events
* unique visitors
* entries
* exits
* conversion rate
* queue depth
* average dwell

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

Current processed store:

```text
STORE_001
```

Metrics generated from:

* 58 CV-generated events
* Multiple tracked visitors
* Zone-level analytics

---

## Future Improvements

* Multi-camera identity matching
* Queue estimation
* Real-time streaming
* Interactive dashboard
* Advanced conversion analytics

---

## Author

Soumya Verma
B.Tech Final Year, Madan Mohan Malaviya University of Technology
Store Intelligence Assessment Submission
