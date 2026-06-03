# Live Dashboard

## Overview

The Live Dashboard provides a lightweight real-time monitoring interface for store analytics.

The dashboard retrieves data from the Metrics API and displays key operational metrics.

## Run Dashboard

Start the FastAPI application first:

```bash
uvicorn app.main:app --reload
```

Then open another terminal and run:

```bash
python dashboard/live_dashboard.py
```

## Displayed Metrics

* Total Events
* Unique Visitors
* Entries
* Exits
* Conversion Rate
* Queue Depth
* Abandonment Rate

## Refresh Interval

The dashboard automatically refreshes every 5 seconds by querying:

```text
GET /stores/STORE_001/metrics
```

## Example Output

```text
STORE INTELLIGENCE LIVE DASHBOARD
========================================
Store ID: STORE_001
Total Events: 122
Unique Visitors: 20
Entries: 37
Exits: 35
Conversion Rate: 0.0%
Queue Depth: 0
Abandonment Rate: 0%
========================================
Refreshing every 5 seconds...
```
