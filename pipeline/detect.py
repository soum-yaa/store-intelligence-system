import cv2
from ultralytics import YOLO


VIDEO_PATH = r"data/raw/CCTV Footage-20260529T160731Z-3-00144614ea/CCTV Footage/CAM 3.mp4"


def main():
    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("Could not open video:", VIDEO_PATH)
        return

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # Process every 10th frame to keep it fast
        if frame_count % 10 != 0:
            continue

        results = model(frame, classes=[0], conf=0.35, verbose=False)

        person_count = 0

        for result in results:
            boxes = result.boxes
            person_count = len(boxes)

        print(f"Frame {frame_count}: persons detected = {person_count}")

    cap.release()


if __name__ == "__main__":
    main()