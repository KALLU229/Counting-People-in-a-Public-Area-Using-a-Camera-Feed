import cv2
import logging
import threading
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# -------------------------------
# Setup Logging
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# -------------------------------
# Trackable Object Class
# -------------------------------
class TrackableObject:
    def __init__(self, objectID, centroid):
        self.objectID = objectID
        self.centroids = [centroid]
        self.counted = False


# -------------------------------
# Load YOLOv8 model
# -------------------------------
model = YOLO("yolov8n.pt")


# -------------------------------
# Initialize DeepSORT tracker
# -------------------------------
tracker = DeepSort(max_age=30)


# -------------------------------
# Global Counters
# -------------------------------
total_enter = 0
total_exit = 0
trackableObjects = {}
current_inside = 0


# -------------------------------
# Video Processing
# -------------------------------
def process_video(input_path, output_path):

    global total_enter, total_exit, current_inside

    cap = cv2.VideoCapture(input_path)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps,
                          (frame_width, frame_height))

    H = frame_height
    W = frame_width

    logger.info("Processing started...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # -------------------------------
        # YOLO Detection
        # -------------------------------
        results = model(frame)[0]
        detections = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            if cls_id == 0 and conf > 0.5:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                w, h = x2 - x1, y2 - y1
                detections.append(([x1, y1, w, h], conf, "person"))

        # -------------------------------
        # DeepSORT Tracking
        # -------------------------------
        tracks = tracker.update_tracks(detections, frame=frame)

        cv2.line(frame, (0, H // 2), (W, H // 2), (0, 0, 0), 2)

        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            l, t, r, b = map(int, track.to_ltrb())
            centroid = ((l + r) // 2, (t + b) // 2)

            to = trackableObjects.get(track_id)

            # First time seeing this ID
            if to is None:
                to = TrackableObject(track_id, centroid)

            else:
                y = [c[1] for c in to.centroids]
                direction = centroid[1] - sum(y) / len(y)
                to.centroids.append(centroid)

                # Count movement
                if not to.counted:
                    if direction < 0 and centroid[1] < H // 2:
                        total_exit += 1
                        current_inside -= 1
                        to.counted = True
                        logger.info(f"Person EXIT — ID {track_id}")

                    elif direction > 0 and centroid[1] > H // 2:
                        total_enter += 1
                        current_inside += 1
                        to.counted = True
                        logger.info(f"Person ENTER — ID {track_id}")

            trackableObjects[track_id] = to

            # Draw bbox + ID
            cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
            cv2.putText(frame, f"ID {track_id}", (l, t - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 255, 0), 2)

        # Display stats
        cv2.putText(frame, f"Entered: {total_enter}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.putText(frame, f"Exited: {total_exit}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.putText(frame, f"Inside: {current_inside}", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 150, 0), 2)

        out.write(frame)
        cv2.imshow("YOLOv8 + DeepSORT People Counter", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    logger.info("Processing finished.")
    logger.info(f"ENTERED = {total_enter}")
    logger.info(f"EXITED = {total_exit}")
    logger.info(f"CURRENT INSIDE = {current_inside}")


# -------------------------------
# Thread Wrapper
# -------------------------------
def start_thread(input_path, output_path):
    t = threading.Thread(target=process_video,
                         args=(input_path, output_path))
    t.start()


# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    input_path = input("Enter video path: ")
    output_path = input("Enter output path: ")

    start_thread(input_path, output_path)
