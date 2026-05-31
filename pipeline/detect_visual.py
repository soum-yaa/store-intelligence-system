import cv2
from ultralytics import YOLO


VIDEO_PATH = r"data/raw/CCTV Footage-20260529T160731Z-3-00144614ea/CCTV Footage/CAM 3.mp4"
OUTPUT_PATH = r"output/cam3_detected.mp4"


def main():
    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("Could not open video:", VIDEO_PATH)
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        results = model(frame, classes=[0], conf=0.35, verbose=False)

        annotated_frame = results[0].plot()

        out.write(annotated_frame)

        if frame_count % 100 == 0:
            print(f"Processed {frame_count} frames")

    cap.release()
    out.release()

    print("Done. Output saved at:", OUTPUT_PATH)


if __name__ == "__main__":
    main()