import cv2
import os
import time
from collections import Counter
from ultralytics import YOLO


# ==========================================
# CONFIGURATION
# ==========================================

INPUT_VIDEO = "input/video.mp4"
OUTPUT_VIDEO = "output/analytics_video.mp4"
MODEL_PATH = "models/yolo11n.pt"

CONFIDENCE = 0.50
IOU = 0.45

# 0.50 = center of video
LINE_POSITION = 0.50


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

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


if video_fps <= 0:

    video_fps = 30


video_duration = total_frames / video_fps


print(f"Resolution: {width} x {height}")
print(f"FPS: {video_fps}")
print(f"Total video frames: {total_frames}")
print(f"Video duration: {video_duration:.2f} seconds")


# ==========================================
# COUNTING LINE
# ==========================================

line_x = int(width * LINE_POSITION)

print(f"Counting line X position: {line_x}")


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


if not out.isOpened():

    print("ERROR: Could not create output video.")

    cap.release()

    exit()


# ==========================================
# TRACKING VARIABLES
# ==========================================

frame_count = 0

start_time = time.time()


# All unique tracking IDs
unique_track_ids = set()


# Previous X position of every object
previous_positions = {}


# IDs already counted
counted_ids = set()


# ==========================================
# TOTAL ENTRY / EXIT
# ==========================================

entered_count = 0

exited_count = 0


# ==========================================
# CLASS-WISE ENTRY / EXIT
# ==========================================

entered_by_class = Counter()

exited_by_class = Counter()


# ==========================================
# CLASS STATISTICS
# ==========================================

total_class_counts = Counter()


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
    # DRAW YOLO RESULTS
    # ======================================

    annotated_frame = result.plot()


    # ======================================
    # OBJECT COUNTERS
    # ======================================

    class_counter = Counter()

    current_objects = 0


    # ======================================
    # PROCESS DETECTED OBJECTS
    # ======================================

    if result.boxes is not None:

        if result.boxes.id is not None:

            track_ids = result.boxes.id.int().cpu().tolist()

            class_ids = result.boxes.cls.int().cpu().tolist()

            confidences = result.boxes.conf.cpu().tolist()

            xyxy = result.boxes.xyxy.cpu().tolist()


            # ==================================
            # LOOP THROUGH OBJECTS
            # ==================================

            for track_id, class_id, confidence, box in zip(

                track_ids,

                class_ids,

                confidences,

                xyxy

            ):

                current_objects += 1


                # ==================================
                # UNIQUE TRACK ID
                # ==================================

                unique_track_ids.add(track_id)


                # ==================================
                # CLASS NAME
                # ==================================

                class_name = model.names[class_id]


                class_counter[class_name] += 1

                total_class_counts[class_name] += 1


                # ==================================
                # BOUNDING BOX
                # ==================================

                x1, y1, x2, y2 = box


                center_x = int((x1 + x2) / 2)

                center_y = int((y1 + y2) / 2)


                # ==================================
                # DRAW CENTER POINT
                # ==================================

                cv2.circle(

                    annotated_frame,

                    (center_x, center_y),

                    5,

                    (0, 255, 255),

                    -1

                )


                # ==================================
                # TRACK ID LABEL
                # ==================================

                label = (

                    f"ID:{track_id} "

                    f"{class_name} "

                    f"{confidence:.2f}"

                )


                cv2.putText(

                    annotated_frame,

                    label,

                    (center_x - 60, center_y - 12),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.50,

                    (255, 255, 255),

                    2

                )


                # ==================================
                # LINE CROSSING
                # ==================================

                if track_id in previous_positions:

                    previous_x = previous_positions[track_id]


                    # ==================================
                    # LEFT -> RIGHT
                    # ENTERED
                    # ==================================

                    if (

                        previous_x < line_x

                        and center_x >= line_x

                        and track_id not in counted_ids

                    ):

                        entered_count += 1

                        entered_by_class[class_name] += 1

                        counted_ids.add(track_id)


                        print(

                            f"ENTERED: "

                            f"ID {track_id} - "

                            f"{class_name}"

                        )


                    # ==================================
                    # RIGHT -> LEFT
                    # EXITED
                    # ==================================

                    elif (

                        previous_x > line_x

                        and center_x <= line_x

                        and track_id not in counted_ids

                    ):

                        exited_count += 1

                        exited_by_class[class_name] += 1

                        counted_ids.add(track_id)


                        print(

                            f"EXITED: "

                            f"ID {track_id} - "

                            f"{class_name}"

                        )


                # ==================================
                # SAVE CURRENT POSITION
                # ==================================

                previous_positions[track_id] = center_x


    # ======================================
    # DRAW COUNTING LINE
    # ======================================

    cv2.line(

        annotated_frame,

        (line_x, 0),

        (line_x, height),

        (255, 0, 255),

        4

    )


    # ======================================
    # COUNTING LINE LABEL
    # ======================================

    cv2.putText(

        annotated_frame,

        "COUNTING LINE",

        (line_x + 10, 40),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.65,

        (255, 0, 255),

        2

    )


    # ======================================
    # PROCESSING FPS
    # ======================================

    elapsed_time = time.time() - start_time


    if elapsed_time > 0:

        processing_fps = frame_count / elapsed_time

    else:

        processing_fps = 0


    # ======================================
    # VIDEO PROGRESS
    # ======================================

    if total_frames > 0:

        progress = (

            frame_count / total_frames

        ) * 100

    else:

        progress = 0


    # ======================================
    # CURRENT VIDEO TIME
    # ======================================

    current_video_time = frame_count / video_fps


    # ======================================
    # TOTAL CROSSINGS
    # ======================================

    total_crossings = (

        entered_count +

        exited_count

    )


    # ======================================
    # DASHBOARD
    # ======================================

    cv2.rectangle(

        annotated_frame,

        (10, 10),

        (470, 470),

        (0, 0, 0),

        -1

    )


    # ======================================
    # TITLE
    # ======================================

    cv2.putText(

        annotated_frame,

        "YOLO VIDEO ANALYTICS",

        (25, 40),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.75,

        (0, 255, 0),

        2

    )


    # ======================================
    # PROCESSING FPS
    # ======================================

    cv2.putText(

        annotated_frame,

        f"Processing FPS: {processing_fps:.2f}",

        (25, 70),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.55,

        (255, 255, 255),

        2

    )


    # ======================================
    # CURRENT OBJECTS
    # ======================================

    cv2.putText(

        annotated_frame,

        f"Current Objects: {current_objects}",

        (25, 100),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.60,

        (255, 255, 255),

        2

    )


    # ======================================
    # UNIQUE OBJECTS
    # ======================================

    cv2.putText(

        annotated_frame,

        f"Unique IDs: {len(unique_track_ids)}",

        (25, 130),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.60,

        (255, 255, 255),

        2

    )


    # ======================================
    # TOTAL ENTRY / EXIT
    # ======================================

    cv2.putText(

        annotated_frame,

        f"ENTERED: {entered_count}",

        (25, 165),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.65,

        (0, 255, 0),

        2

    )


    cv2.putText(

        annotated_frame,

        f"EXITED: {exited_count}",

        (220, 165),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.65,

        (0, 0, 255),

        2

    )


    # ======================================
    # TOTAL CROSSINGS
    # ======================================

    cv2.putText(

        annotated_frame,

        f"Total Crossings: {total_crossings}",

        (25, 200),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.60,

        (0, 255, 255),

        2

    )


    # ======================================
    # VIDEO TIME
    # ======================================

    cv2.putText(

        annotated_frame,

        f"Video Time: {current_video_time:.1f}s",

        (25, 230),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.60,

        (255, 255, 255),

        2

    )


    # ======================================
    # PROGRESS
    # ======================================

    cv2.putText(

        annotated_frame,

        f"Progress: {progress:.1f}%",

        (25, 260),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.60,

        (255, 255, 255),

        2

    )


    # ======================================
    # CONFIDENCE
    # ======================================

    cv2.putText(

        annotated_frame,

        f"Confidence: {CONFIDENCE:.2f}",

        (25, 290),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.55,

        (255, 255, 255),

        2

    )


    # ======================================
    # CLASS-WISE ENTRY STATISTICS
    # ======================================

    cv2.putText(

        annotated_frame,

        "ENTRY BY CLASS",

        (25, 325),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.60,

        (0, 255, 0),

        2

    )


    y_entry = 350


    for class_name, count in entered_by_class.items():

        text = f"{class_name}: {count}"

        cv2.putText(

            annotated_frame,

            text,

            (25, y_entry),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.50,

            (0, 255, 0),

            2

        )

        y_entry += 25


    # ======================================
    # CLASS-WISE EXIT STATISTICS
    # ======================================

    cv2.putText(

        annotated_frame,

        "EXIT BY CLASS",

        (220, 325),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.60,

        (0, 0, 255),

        2

    )


    y_exit = 350


    for class_name, count in exited_by_class.items():

        text = f"{class_name}: {count}"

        cv2.putText(

            annotated_frame,

            text,

            (220, y_exit),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.50,

            (0, 0, 255),

            2

        )

        y_exit += 25


    # ======================================
    # CURRENT CLASS COUNTS
    # ======================================

    y_class = max(y_entry, y_exit) + 15


    for class_name, count in class_counter.items():

        text = f"{class_name}: {count}"

        cv2.putText(

            annotated_frame,

            text,

            (25, y_class),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.55,

            (255, 255, 0),

            2

        )

        y_class += 25


    # ======================================
    # SAVE FRAME
    # ======================================

    out.write(annotated_frame)


    # ======================================
    # SHOW VIDEO
    # ======================================

    cv2.imshow(

        "YOLO Video Analytics",

        annotated_frame

    )


    # ======================================
    # PRESS Q TO STOP
    # ======================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        print("Processing stopped by user.")

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

total_processing_time = (

    time.time() - start_time

)


average_fps = (

    frame_count /

    total_processing_time

    if total_processing_time > 0

    else 0

)


total_crossings = (

    entered_count +

    exited_count

)


print("\n========================================")

print("VIDEO ANALYTICS COMPLETED")

print("========================================")

print(

    f"Total frames processed: "

    f"{frame_count}"

)

print(

    f"Unique objects tracked: "

    f"{len(unique_track_ids)}"

)

print(

    f"Objects entered: "

    f"{entered_count}"

)

print(

    f"Objects exited: "

    f"{exited_count}"

)

print(

    f"Total crossings: "

    f"{total_crossings}"

)

print(

    f"Average processing FPS: "

    f"{average_fps:.2f}"

)

print(

    f"Processing time: "

    f"{total_processing_time:.2f} seconds"

)


# ==========================================
# CLASS-WISE FINAL SUMMARY
# ==========================================

print("\n========================================")

print("ENTRY BY CLASS")

print("========================================")


if entered_by_class:

    for class_name, count in entered_by_class.items():

        print(

            f"{class_name}: "

            f"{count}"

        )

else:

    print("No objects entered.")


print("\n========================================")

print("EXIT BY CLASS")

print("========================================")


if exited_by_class:

    for class_name, count in exited_by_class.items():

        print(

            f"{class_name}: "

            f"{count}"

        )

else:

    print("No objects exited.")


print("\n========================================")

print(

    f"Output saved to: "

    f"{OUTPUT_VIDEO}"

)

print("========================================")