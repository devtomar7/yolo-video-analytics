import cv2
import os
import time
import csv
import json

from collections import Counter
from ultralytics import YOLO


# ==========================================
# CONFIGURATION
# ==========================================

INPUT_VIDEO = "input/video.mp4"

OUTPUT_VIDEO = "output/analytics_video.mp4"

CSV_REPORT = "output/analytics_report.csv"

JSON_REPORT = "output/analytics_summary.json"

TIME_SERIES_REPORT = "output/analytics_timeseries.csv"

MODEL_PATH = "models/yolo11n.pt"


CONFIDENCE = 0.50

IOU = 0.45


# ==========================================
# COUNTING LINE CONFIGURATION
# ==========================================

# 0.50 = center of video
LINE_POSITION = 0.50

# Prevent unstable crossing detection
LINE_TOLERANCE = 30


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

    print(
        f"ERROR: Could not open video: "
        f"{INPUT_VIDEO}"
    )

    exit()


# ==========================================
# VIDEO INFORMATION
# ==========================================

width = int(
    cap.get(cv2.CAP_PROP_FRAME_WIDTH)
)

height = int(
    cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
)

video_fps = cap.get(
    cv2.CAP_PROP_FPS
)

total_frames = int(
    cap.get(cv2.CAP_PROP_FRAME_COUNT)
)


if video_fps <= 0:

    video_fps = 30


video_duration = (
    total_frames / video_fps
    if video_fps > 0
    else 0
)


print(
    f"Resolution: "
    f"{width} x {height}"
)

print(
    f"FPS: "
    f"{video_fps}"
)

print(
    f"Total video frames: "
    f"{total_frames}"
)

print(
    f"Video duration: "
    f"{video_duration:.2f} seconds"
)


# ==========================================
# COUNTING LINE
# ==========================================

line_x = int(
    width * LINE_POSITION
)


print(
    f"Counting line X position: "
    f"{line_x}"
)

print(
    f"Line tolerance: "
    f"{LINE_TOLERANCE}px"
)


# ==========================================
# VIDEO WRITER
# ==========================================

fourcc = cv2.VideoWriter_fourcc(
    *"mp4v"
)


out = cv2.VideoWriter(

    OUTPUT_VIDEO,

    fourcc,

    video_fps,

    (width, height)

)


if not out.isOpened():

    print(
        "ERROR: Could not create output video."
    )

    cap.release()

    exit()


# ==========================================
# PROCESSING VARIABLES
# ==========================================

frame_count = 0

start_time = time.time()


# ==========================================
# UNIQUE TRACK IDS
# ==========================================

unique_track_ids = set()


# ==========================================
# PREVIOUS OBJECT POSITIONS
# ==========================================

previous_positions = {}


# ==========================================
# COUNTED OBJECT IDS
# ==========================================

counted_ids = set()


# ==========================================
# ENTRY / EXIT COUNTERS
# ==========================================

entered_count = 0

exited_count = 0


# ==========================================
# CLASS-WISE ENTRY / EXIT
# ==========================================

entered_by_class = Counter()

exited_by_class = Counter()


# ==========================================
# CLASS DETECTION STATISTICS
# ==========================================

total_class_counts = Counter()


# ==========================================
# PER-TRACK ANALYTICS
# ==========================================

track_data = {}


# ==========================================
# TIME-SERIES ANALYTICS
# ==========================================

timeseries_data = []


# ==========================================
# LAST CURRENT OBJECT COUNT
# ==========================================

last_current_objects = 0


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
    # CURRENT OBJECT COUNTERS
    # ======================================

    class_counter = Counter()

    current_objects = 0


    # ======================================
    # PROCESS DETECTED OBJECTS
    # ======================================

    if (

        result.boxes is not None

        and result.boxes.id is not None

    ):


        track_ids = (

            result.boxes.id

            .int()

            .cpu()

            .tolist()

        )


        class_ids = (

            result.boxes.cls

            .int()

            .cpu()

            .tolist()

        )


        confidences = (

            result.boxes.conf

            .cpu()

            .tolist()

        )


        xyxy = (

            result.boxes.xyxy

            .cpu()

            .tolist()

        )


        # ==================================
        # LOOP THROUGH OBJECTS
        # ==================================

        for (

            track_id,

            class_id,

            confidence,

            box

        ) in zip(

            track_ids,

            class_ids,

            confidences,

            xyxy

        ):


            current_objects += 1


            # ==================================
            # UNIQUE TRACK ID
            # ==================================

            unique_track_ids.add(
                track_id
            )


            # ==================================
            # CLASS NAME
            # ==================================

            class_name = model.names[
                class_id
            ]


            class_counter[
                class_name
            ] += 1


            total_class_counts[
                class_name
            ] += 1


            # ==================================
            # BOUNDING BOX
            # ==================================

            x1, y1, x2, y2 = box


            center_x = int(
                (x1 + x2) / 2
            )


            center_y = int(
                (y1 + y2) / 2
            )


            # ==================================
            # TRACK DATA INITIALIZATION
            # ==================================

            if track_id not in track_data:

                track_data[track_id] = {

                    "track_id":
                        track_id,

                    "class":
                        class_name,

                    "first_frame":
                        frame_count,

                    "last_frame":
                        frame_count,

                    "frames_tracked":
                        1,

                    "first_x":
                        center_x,

                    "last_x":
                        center_x,

                    "max_confidence":
                        float(confidence),

                    "entry":
                        False,

                    "exit":
                        False,

                    "direction":
                        "none",

                    "entry_frame":
                        None,

                    "exit_frame":
                        None

                }


            else:

                track_data[
                    track_id
                ][
                    "last_frame"
                ] = frame_count


                track_data[
                    track_id
                ][
                    "frames_tracked"
                ] += 1


                track_data[
                    track_id
                ][
                    "last_x"
                ] = center_x


                track_data[
                    track_id
                ][
                    "max_confidence"
                ] = max(

                    track_data[
                        track_id
                    ][
                        "max_confidence"
                    ],

                    float(confidence)

                )


            # ==================================
            # DRAW CENTER POINT
            # ==================================

            cv2.circle(

                annotated_frame,

                (
                    center_x,
                    center_y
                ),

                6,

                (0, 255, 255),

                -1

            )


            # ==================================
            # TRACK LABEL
            # ==================================

            label = (

                f"ID:{track_id} "

                f"{class_name} "

                f"{confidence:.2f}"

            )


            cv2.putText(

                annotated_frame,

                label,

                (
                    center_x - 70,
                    center_y - 12
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.50,

                (255, 255, 255),

                2

            )


            # ==================================
            # LINE CROSSING
            # ==================================

            if track_id in previous_positions:

                previous_x = (
                    previous_positions[
                        track_id
                    ]
                )


                # ==================================
                # LEFT -> RIGHT
                # ENTERED
                # ==================================

                if (

                    previous_x
                    < line_x - LINE_TOLERANCE

                    and center_x
                    >= line_x + LINE_TOLERANCE

                    and track_id
                    not in counted_ids

                ):


                    entered_count += 1


                    entered_by_class[
                        class_name
                    ] += 1


                    counted_ids.add(
                        track_id
                    )


                    track_data[
                        track_id
                    ][
                        "entry"
                    ] = True


                    track_data[
                        track_id
                    ][
                        "direction"
                    ] = "left_to_right"


                    track_data[
                        track_id
                    ][
                        "entry_frame"
                    ] = frame_count


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

                    previous_x
                    > line_x + LINE_TOLERANCE

                    and center_x
                    <= line_x - LINE_TOLERANCE

                    and track_id
                    not in counted_ids

                ):


                    exited_count += 1


                    exited_by_class[
                        class_name
                    ] += 1


                    counted_ids.add(
                        track_id
                    )


                    track_data[
                        track_id
                    ][
                        "exit"
                    ] = True


                    track_data[
                        track_id
                    ][
                        "direction"
                    ] = "right_to_left"


                    track_data[
                        track_id
                    ][
                        "exit_frame"
                    ] = frame_count


                    print(

                        f"EXITED: "

                        f"ID {track_id} - "

                        f"{class_name}"

                    )


            # ==================================
            # SAVE CURRENT POSITION
            # ==================================

            previous_positions[
                track_id
            ] = center_x


    # ======================================
    # SAVE CURRENT OBJECT COUNT
    # ======================================

    last_current_objects = current_objects


    # ======================================
    # DRAW COUNTING LINE
    # ======================================

    cv2.line(

        annotated_frame,

        (line_x, 0),

        (line_x, height),

        (255, 0, 255),

        5

    )


    # ======================================
    # LINE LABEL
    # ======================================

    cv2.putText(

        annotated_frame,

        "COUNTING LINE",

        (
            line_x + 15,
            45
        ),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.75,

        (255, 0, 255),

        2

    )


    # ======================================
    # PROCESSING FPS
    # ======================================

    elapsed_time = (

        time.time()

        - start_time

    )


    processing_fps = (

        frame_count / elapsed_time

        if elapsed_time > 0

        else 0

    )


    # ======================================
    # VIDEO PROGRESS
    # ======================================

    progress = (

        (

            frame_count

            / total_frames

        ) * 100

        if total_frames > 0

        else 0

    )


    # ======================================
    # VIDEO TIME
    # ======================================

    current_video_time = (

        frame_count

        / video_fps

    )


    # ======================================
    # TOTAL CROSSINGS
    # ======================================

    total_crossings = (

        entered_count

        + exited_count

    )


    # ======================================
    # NET COUNT
    # ======================================

    net_count = (

        entered_count

        - exited_count

    )


    # ======================================
    # TIME-SERIES DATA
    # ======================================

    timeseries_data.append({

        "frame":
            frame_count,

        "time_seconds":
            round(
                current_video_time,
                2
            ),

        "current_objects":
            current_objects,

        "entered":
            entered_count,

        "exited":
            exited_count,

        "total_crossings":
            total_crossings,

        "net_count":
            net_count,

        "processing_fps":
            round(
                processing_fps,
                2
            )

    })


    # ======================================
    # DASHBOARD BACKGROUND
    # ======================================

    cv2.rectangle(

        annotated_frame,

        (10, 10),

        (500, 500),

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
    # ENTERED
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


    # ======================================
    # EXITED
    # ======================================

    cv2.putText(

        annotated_frame,

        f"EXITED: {exited_count}",

        (230, 165),

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
    # NET COUNT
    # ======================================

    cv2.putText(

        annotated_frame,

        f"Net Count: {net_count}",

        (25, 230),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.60,

        (255, 255, 255),

        2

    )


    # ======================================
    # VIDEO TIME
    # ======================================

    cv2.putText(

        annotated_frame,

        f"Video Time: {current_video_time:.1f}s",

        (25, 260),

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

        (25, 290),

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

        (25, 320),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.55,

        (255, 255, 255),

        2

    )


    # ======================================
    # ENTRY BY CLASS
    # ======================================

    cv2.putText(

        annotated_frame,

        "ENTRY BY CLASS",

        (25, 355),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.55,

        (0, 255, 0),

        2

    )


    y_entry = 380


    for class_name, count in (
        entered_by_class.items()
    ):

        cv2.putText(

            annotated_frame,

            f"{class_name}: {count}",

            (25, y_entry),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.50,

            (0, 255, 0),

            2

        )

        y_entry += 25


    # ======================================
    # EXIT BY CLASS
    # ======================================

    cv2.putText(

        annotated_frame,

        "EXIT BY CLASS",

        (230, 355),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.55,

        (0, 0, 255),

        2

    )


    y_exit = 380


    for class_name, count in (
        exited_by_class.items()
    ):

        cv2.putText(

            annotated_frame,

            f"{class_name}: {count}",

            (230, y_exit),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.50,

            (0, 0, 255),

            2

        )

        y_exit += 25


    # ======================================
    # SAVE FRAME
    # ======================================

    out.write(
        annotated_frame
    )


    # ======================================
    # DISPLAY VIDEO
    # ======================================

    cv2.imshow(

        "YOLO Video Analytics",

        annotated_frame

    )


    # ======================================
    # PRESS Q TO STOP
    # ======================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        print(
            "Processing stopped by user."
        )

        break


# ==========================================
# CLEANUP
# ==========================================

cap.release()

out.release()

cv2.destroyAllWindows()


# ==========================================
# FINAL PROCESSING STATISTICS
# ==========================================

total_processing_time = (

    time.time()

    - start_time

)


average_fps = (

    frame_count
    / total_processing_time

    if total_processing_time > 0

    else 0

)


total_crossings = (

    entered_count
    + exited_count

)


net_count = (

    entered_count
    - exited_count

)


# ==========================================
# CLASS-WISE UNIQUE OBJECTS
# ==========================================

unique_objects_by_class = Counter()


for data in track_data.values():

    unique_objects_by_class[
        data["class"]
    ] += 1


# ==========================================
# CREATE CSV REPORT
# ==========================================

with open(

    CSV_REPORT,

    "w",

    newline="",

    encoding="utf-8"

) as csv_file:


    writer = csv.writer(
        csv_file
    )


    writer.writerow([

        "Track ID",

        "Class",

        "First Frame",

        "Last Frame",

        "Frames Tracked",

        "Max Confidence",

        "First X",

        "Last X",

        "Entry",

        "Exit",

        "Direction",

        "Entry Frame",

        "Exit Frame"

    ])


    for track_id in sorted(
        track_data.keys()
    ):


        data = track_data[
            track_id
        ]


        writer.writerow([

            data["track_id"],

            data["class"],

            data["first_frame"],

            data["last_frame"],

            data["frames_tracked"],

            f'{data["max_confidence"]:.3f}',

            data["first_x"],

            data["last_x"],

            data["entry"],

            data["exit"],

            data["direction"],

            data["entry_frame"],

            data["exit_frame"]

        ])


print(

    f"\nAnalytics report saved to: "

    f"{CSV_REPORT}"

)


# ==========================================
# CREATE TIME-SERIES CSV
# ==========================================

with open(

    TIME_SERIES_REPORT,

    "w",

    newline="",

    encoding="utf-8"

) as csv_file:


    writer = csv.writer(
        csv_file
    )


    writer.writerow([

        "Frame",

        "Time Seconds",

        "Current Objects",

        "Entered",

        "Exited",

        "Total Crossings",

        "Net Count",

        "Processing FPS"

    ])


    for row in timeseries_data:

        writer.writerow([

            row["frame"],

            row["time_seconds"],

            row["current_objects"],

            row["entered"],

            row["exited"],

            row["total_crossings"],

            row["net_count"],

            row["processing_fps"]

        ])


print(

    f"Time-series report saved to: "

    f"{TIME_SERIES_REPORT}"

)


# ==========================================
# JSON SUMMARY
# ==========================================

summary = {

    "video": {

        "input":
            INPUT_VIDEO,

        "output":
            OUTPUT_VIDEO,

        "width":
            width,

        "height":
            height,

        "fps":
            video_fps,

        "total_frames":
            total_frames,

        "duration_seconds":
            round(
                video_duration,
                2
            )

    },


    "model": {

        "model_path":
            MODEL_PATH,

        "confidence":
            CONFIDENCE,

        "iou":
            IOU,

        "tracker":
            "ByteTrack"

    },


    "counting_line": {

        "position":
            LINE_POSITION,

        "x":
            line_x,

        "tolerance":
            LINE_TOLERANCE

    },


    "analytics": {

        "unique_objects":
            len(unique_track_ids),

        "current_objects":
            last_current_objects,

        "entered":
            entered_count,

        "exited":
            exited_count,

        "total_crossings":
            total_crossings,

        "net_count":
            net_count

    },


    "class_statistics": {

        "unique_objects_by_class":
            dict(
                unique_objects_by_class
            ),

        "detections_by_class":
            dict(
                total_class_counts
            ),

        "entered_by_class":
            dict(
                entered_by_class
            ),

        "exited_by_class":
            dict(
                exited_by_class
            )

    },


    "processing": {

        "frames_processed":
            frame_count,

        "processing_time_seconds":
            round(
                total_processing_time,
                2
            ),

        "average_processing_fps":
            round(
                average_fps,
                2
            )

    },


    "reports": {

        "csv":
            CSV_REPORT,

        "json":
            JSON_REPORT,

        "timeseries":
            TIME_SERIES_REPORT

    }

}


# ==========================================
# SAVE JSON
# ==========================================

with open(

    JSON_REPORT,

    "w",

    encoding="utf-8"

) as json_file:


    json.dump(

        summary,

        json_file,

        indent=4

    )


print(

    f"JSON summary saved to: "

    f"{JSON_REPORT}"

)


# ==========================================
# FINAL TERMINAL SUMMARY
# ==========================================

print(
    "\n========================================"
)

print(
    "VIDEO ANALYTICS COMPLETED"
)

print(
    "========================================"
)


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

    f"Net count: "

    f"{net_count}"

)


print(

    f"Final current objects: "

    f"{last_current_objects}"

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
# ENTRY SUMMARY
# ==========================================

print(
    "\n========================================"
)

print(
    "ENTRY BY CLASS"
)

print(
    "========================================"
)


if entered_by_class:

    for class_name, count in (
        entered_by_class.items()
    ):

        print(
            f"{class_name}: {count}"
        )

else:

    print(
        "No objects entered."
    )


# ==========================================
# EXIT SUMMARY
# ==========================================

print(
    "\n========================================"
)

print(
    "EXIT BY CLASS"
)

print(
    "========================================"
)


if exited_by_class:

    for class_name, count in (
        exited_by_class.items()
    ):

        print(
            f"{class_name}: {count}"
        )

else:

    print(
        "No objects exited."
    )


# ==========================================
# UNIQUE OBJECTS BY CLASS
# ==========================================

print(
    "\n========================================"
)

print(
    "UNIQUE OBJECTS BY CLASS"
)

print(
    "========================================"
)


for class_name, count in (
    unique_objects_by_class.items()
):

    print(
        f"{class_name}: {count}"
    )


# ==========================================
# DETECTIONS BY CLASS
# ==========================================

print(
    "\n========================================"
)

print(
    "TOTAL DETECTIONS BY CLASS"
)

print(
    "========================================"
)


for class_name, count in (
    total_class_counts.items()
):

    print(
        f"{class_name}: {count}"
    )


# ==========================================
# FINAL OUTPUT
# ==========================================

print(
    "\n========================================"
)

print(
    f"Output video: "
    f"{OUTPUT_VIDEO}"
)

print(
    f"Analytics CSV: "
    f"{CSV_REPORT}"
)

print(
    f"Analytics JSON: "
    f"{JSON_REPORT}"
)

print(
    f"Time-series CSV: "
    f"{TIME_SERIES_REPORT}"
)

print(
    "========================================"
)