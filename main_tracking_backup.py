import cv2
import os
import time
from collections import Counter
from ultralytics import YOLO


# ==========================================
# CONFIGURATION
# ==========================================

INPUT_VIDEO = "input/video.mp4"
OUTPUT_VIDEO = "output/tracked_video.mp4"
MODEL_PATH = "models/yolo11n.pt"

CONFIDENCE = 0.50
IOU = 0.45


# ==========================================
# CREATE OUTPUT DIRECTORY
# ==========================================

os.makedirs("output", exist_ok=True)


# ==========================================
# LOAD YOLO MODEL
# ==========================================

print("Loading YOLO model...")

model = YOLO(MODEL_PATH)

print("YOLO model loaded successfully!")


# ==========================================
# OPEN VIDEO
# ==========================================

cap = cv2.VideoCapture(INPUT_VIDEO)

if not cap.isOpened():
    print(f"ERROR: Could not open video: {INPUT_VIDEO}")
    exit()


# ==========================================
# VIDEO INFORMATION
# ==========================================

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_fps = cap.get(cv2.CAP_PROP_FPS)

if video_fps <= 0:
    video_fps = 30

print(f"Resolution: {width} x {height}")
print(f"FPS: {video_fps}")


# ==========================================
# VIDEO WRITER
# ==========================================

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

out = cv2.VideoWriter(
    OUTPUT_VIDEO,
    fourcc,
    video_fps,
    (width, height)
)


# ==========================================
# TRACKING VARIABLES
# ==========================================

frame_count = 0
start_time = time.time()

# Store unique IDs that appeared
unique_track_ids = set()


# ==========================================
# PROCESS VIDEO
# ==========================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1


    # ======================================
    # YOLO TRACKING
    # ======================================

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=CONFIDENCE,
        iou=IOU,
        verbose=False
    )

    result = results[0]


    # ======================================
    # DRAW TRACKING RESULTS
    # ======================================

    annotated_frame = result.plot()


    # ======================================
    # OBJECT COUNTS
    # ======================================

    class_counter = Counter()


    if result.boxes is not None:

        # Check whether tracking IDs exist
        if result.boxes.id is not None:

            track_ids = result.boxes.id.int().cpu().tolist()
            class_ids = result.boxes.cls.int().cpu().tolist()

            for track_id, class_id in zip(track_ids, class_ids):

                class_name = model.names[class_id]

                class_counter[class_name] += 1

                # Store unique ID
                unique_track_ids.add(track_id)


    # ======================================
    # CALCULATE FPS
    # ======================================

    elapsed_time = time.time() - start_time

    if elapsed_time > 0:
        current_fps = frame_count / elapsed_time
    else:
        current_fps = 0


    # ======================================
    # DISPLAY TITLE
    # ======================================

    cv2.putText(
        annotated_frame,
        "YOLO VIDEO ANALYTICS - TRACKING",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )


    # ======================================
    # DISPLAY FPS
    # ======================================

    cv2.putText(
        annotated_frame,
        f"FPS: {current_fps:.2f}",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )


    # ======================================
    # DISPLAY CURRENT OBJECT COUNTS
    # ======================================

    y_position = 110

    for class_name, count in class_counter.items():

        text = f"{class_name}: {count}"

        cv2.putText(
            annotated_frame,
            text,
            (20, y_position),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 0),
            2
        )

        y_position += 30


    # ======================================
    # DISPLAY UNIQUE TRACKED OBJECTS
    # ======================================

    cv2.putText(
        annotated_frame,
        f"Unique IDs: {len(unique_track_ids)}",
        (20, y_position + 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 255),
        2
    )


    # ======================================
    # SAVE FRAME
    # ======================================

    out.write(annotated_frame)


    # ======================================
    # SHOW VIDEO
    # ======================================

    cv2.imshow(
        "YOLO Video Analytics - Tracking",
        annotated_frame
    )


    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==========================================
# CLEANUP
# ==========================================

cap.release()
out.release()
cv2.destroyAllWindows()


# ==========================================
# FINAL RESULTS
# ==========================================

print("\n========================================")
print("VIDEO TRACKING COMPLETED")
print("========================================")

print(f"Total frames processed: {frame_count}")
print(f"Unique objects tracked: {len(unique_track_ids)}")
print(f"Output saved to: {OUTPUT_VIDEO}")