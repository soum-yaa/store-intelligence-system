import cv2
import json
import uuid
from datetime import datetime, timedelta
from ultralytics import YOLO


VIDEO_PATH = r"data/raw/CCTV Footage-20260529T160731Z-3-00144614ea/CCTV Footage/CAM 1.mp4"
OUTPUT_PATH = r"output/events.jsonl"

STORE_ID = "STORE_001"
CAMERA_ID = "CAM_1"
ZONE_ID = "MAIN_FLOOR"

VIDEO_START_TIME = datetime(2026, 4, 10, 20, 10, 4)


def make_event(visitor_id, event_type, timestamp, dwell_ms=0, session_seq=1):
    return {
        "event_id": str(uuid.uuid4()),
        "store_id": STORE_ID,
        "camera_id": CAMERA_ID,
        "visitor_id": visitor_id,
        "event_type": event_type,
        "timestamp": timestamp.isoformat() + "Z",
        "zone_id": None if event_type in ["ENTRY", "EXIT"] else ZONE_ID,
        "dwell_ms": dwell_ms,
        "is_staff": False,
        "confidence": 0.85,
        "metadata": {
            "queue_depth": None,
            "sku_zone": ZONE_ID,
            "session_seq": session_seq
        }
    }


def main():
    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("Could not open video:", VIDEO_PATH)
        return

    fps = cap.get(cv2.CAP_PROP_FPS)

    active_tracks = {}
    events = []

    frame_count = 0
    process_every_n_frames = 15

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        if frame_count % process_every_n_frames != 0:
            continue

        timestamp = VIDEO_START_TIME + timedelta(seconds=frame_count / fps)

        results = model.track(
            frame,
            classes=[0],
            conf=0.30,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False
        )

        if results[0].boxes.id is None:
            continue

        track_ids = results[0].boxes.id.cpu().numpy().astype(int)

        for track_id in track_ids:
            visitor_id = f"VIS_{track_id}"

            if visitor_id not in active_tracks:
                active_tracks[visitor_id] = {
                    "first_seen": timestamp,
                    "last_seen": timestamp,
                    "dwell_emitted": False,
                    "session_seq": 1
                }

                events.append(
                    make_event(
                        visitor_id,
                        "ENTRY",
                        timestamp,
                        session_seq=1
                    )
                )

                events.append(
                    make_event(
                        visitor_id,
                        "ZONE_ENTER",
                        timestamp,
                        session_seq=2
                    )
                )

            else:
                active_tracks[visitor_id]["last_seen"] = timestamp

                dwell_time = (
                    timestamp - active_tracks[visitor_id]["first_seen"]
                ).total_seconds()

                if dwell_time >= 30 and not active_tracks[visitor_id]["dwell_emitted"]:
                    events.append(
                        make_event(
                            visitor_id,
                            "ZONE_DWELL",
                            timestamp,
                            dwell_ms=int(dwell_time * 1000),
                            session_seq=3
                        )
                    )

                    active_tracks[visitor_id]["dwell_emitted"] = True

    for visitor_id, data in active_tracks.items():
        events.append(
            make_event(
                visitor_id,
                "EXIT",
                data["last_seen"],
                session_seq=4
            )
        )

    cap.release()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")

    print(f"Generated {len(events)} events")
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()