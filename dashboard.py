import os
import csv
import json
import webbrowser
from collections import Counter


# ==========================================
# CONFIGURATION
# ==========================================

JSON_FILE = "output/analytics_summary.json"
CSV_FILE = "output/analytics_report.csv"
TIMESERIES_FILE = "output/analytics_timeseries.csv"

OUTPUT_HTML = "output/analytics_dashboard.html"


# ==========================================
# CHECK FILES
# ==========================================

if not os.path.exists(JSON_FILE):

    print("ERROR: analytics_summary.json not found.")

    print(
        "Run main.py first to generate analytics data."
    )

    exit()


if not os.path.exists(CSV_FILE):

    print("ERROR: analytics_report.csv not found.")

    print(
        "Run main.py first to generate analytics data."
    )

    exit()


# ==========================================
# CREATE OUTPUT DIRECTORY
# ==========================================

os.makedirs("output", exist_ok=True)


# ==========================================
# LOAD JSON SUMMARY
# ==========================================

with open(
    JSON_FILE,
    "r",
    encoding="utf-8"
) as file:

    summary = json.load(file)


# ==========================================
# LOAD TRACK CSV
# ==========================================

track_data = []

with open(
    CSV_FILE,
    "r",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        track_data.append(row)


# ==========================================
# EXTRACT ANALYTICS
# ==========================================

analytics = summary.get(
    "analytics",
    {}
)

class_statistics = summary.get(
    "class_statistics",
    {}
)

video_info = summary.get(
    "video",
    {}
)

model_info = summary.get(
    "model",
    {}
)

processing_info = summary.get(
    "processing",
    {}
)


# ==========================================
# IMPORTANT:
# READ VALUES DIRECTLY FROM JSON
# ==========================================

unique_objects = analytics.get(
    "unique_objects",
    len(track_data)
)

entered = analytics.get(
    "entered",
    0
)

exited = analytics.get(
    "exited",
    0
)

total_crossings = analytics.get(
    "total_crossings",
    entered + exited
)

net_count = analytics.get(
    "net_count",
    entered - exited
)

current_objects = analytics.get(
    "current_objects",
    0
)


# ==========================================
# CLASS STATISTICS
# ==========================================

unique_by_class = class_statistics.get(
    "unique_objects_by_class",
    {}
)

detections_by_class = class_statistics.get(
    "detections_by_class",
    {}
)

entered_by_class = class_statistics.get(
    "entered_by_class",
    {}
)

exited_by_class = class_statistics.get(
    "exited_by_class",
    {}
)


# ==========================================
# VIDEO INFORMATION
# ==========================================

video_width = video_info.get(
    "width",
    0
)

video_height = video_info.get(
    "height",
    0
)

video_fps = video_info.get(
    "fps",
    0
)

total_frames = video_info.get(
    "total_frames",
    0
)

duration = video_info.get(
    "duration_seconds",
    0
)


# ==========================================
# PROCESSING INFORMATION
# ==========================================

processing_fps = processing_info.get(
    "average_processing_fps",
    0
)

processing_time = processing_info.get(
    "processing_time_seconds",
    0
)

frames_processed = processing_info.get(
    "frames_processed",
    0
)


# ==========================================
# MODEL INFORMATION
# ==========================================

model_path = model_info.get(
    "model_path",
    "Unknown"
)

confidence = model_info.get(
    "confidence",
    0
)

iou = model_info.get(
    "iou",
    0
)

tracker = model_info.get(
    "tracker",
    "Unknown"
)


# ==========================================
# CLASS CHART DATA
# ==========================================

class_labels = list(
    unique_by_class.keys()
)

class_values = list(
    unique_by_class.values()
)


class_detection_labels = list(
    detections_by_class.keys()
)

class_detection_values = list(
    detections_by_class.values()
)


# ==========================================
# GENERATE CLASS TABLE
# ==========================================

class_rows = ""

all_classes = set()

all_classes.update(
    unique_by_class.keys()
)

all_classes.update(
    detections_by_class.keys()
)

all_classes.update(
    entered_by_class.keys()
)

all_classes.update(
    exited_by_class.keys()
)


for class_name in sorted(all_classes):

    unique_count = unique_by_class.get(
        class_name,
        0
    )

    detection_count = detections_by_class.get(
        class_name,
        0
    )

    entry_count = entered_by_class.get(
        class_name,
        0
    )

    exit_count = exited_by_class.get(
        class_name,
        0
    )

    class_rows += f"""
    <tr>
        <td>{class_name}</td>
        <td>{unique_count}</td>
        <td>{detection_count}</td>
        <td>{entry_count}</td>
        <td>{exit_count}</td>
    </tr>
    """


# ==========================================
# GENERATE TRACK TABLE
# ==========================================

track_rows = ""

for row in track_data:

    track_rows += f"""
    <tr>
        <td>{row.get("Track ID", "")}</td>
        <td>{row.get("Class", "")}</td>
        <td>{row.get("First Frame", "")}</td>
        <td>{row.get("Last Frame", "")}</td>
        <td>{row.get("Frames Tracked", "")}</td>
        <td>{row.get("Max Confidence", "")}</td>
        <td>{row.get("Entry", "")}</td>
        <td>{row.get("Exit", "")}</td>
        <td>{row.get("Direction", "")}</td>
    </tr>
    """


# ==========================================
# HTML DASHBOARD
# ==========================================

html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>YOLO Video Analytics Dashboard</title>


<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>


<style>

* {{
    box-sizing: border-box;
}}

body {{

    margin: 0;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background:
        #0f172a;

    color:
        #e2e8f0;

}}


.header {{

    background:
        #111827;

    padding:
        25px 40px;

    border-bottom:
        1px solid #334155;

}}


.header h1 {{

    margin:
        0;

    font-size:
        28px;

}}

.header p {{

    margin-top:
        8px;

    color:
        #94a3b8;

}}


.container {{

    padding:
        30px 40px;

}}


.cards {{

    display:
        grid;

    grid-template-columns:
        repeat(6, 1fr);

    gap:
        18px;

    margin-bottom:
        30px;

}}


.card {{

    background:
        #1e293b;

    padding:
        22px;

    border-radius:
        12px;

    border:
        1px solid #334155;

}}


.card-title {{

    color:
        #94a3b8;

    font-size:
        14px;

    margin-bottom:
        10px;

}}


.card-value {{

    font-size:
        30px;

    font-weight:
        bold;

}}


.green {{
    color:
        #22c55e;
}}

.red {{
    color:
        #ef4444;
}}

.yellow {{
    color:
        #facc15;
}}

.blue {{
    color:
        #38bdf8;
}}


.grid {{

    display:
        grid;

    grid-template-columns:
        1fr 1fr;

    gap:
        25px;

    margin-bottom:
        30px;

}}


.panel {{

    background:
        #1e293b;

    border:
        1px solid #334155;

    border-radius:
        12px;

    padding:
        25px;

}}


.panel h2 {{

    margin-top:
        0;

    margin-bottom:
        20px;

    font-size:
        20px;

}}


.chart-container {{

    height:
        320px;

}}


table {{

    width:
        100%;

    border-collapse:
        collapse;

}}


th {{

    text-align:
        left;

    padding:
        12px;

    background:
        #0f172a;

    color:
        #94a3b8;

}}


td {{

    padding:
        12px;

    border-bottom:
        1px solid #334155;

}}


tr:hover {{

    background:
        #263449;

}}


.info-grid {{

    display:
        grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap:
        15px;

}}


.info-box {{

    background:
        #0f172a;

    padding:
        15px;

    border-radius:
        8px;

}}


.info-label {{

    color:
        #94a3b8;

    font-size:
        13px;

}}


.info-value {{

    margin-top:
        5px;

    font-weight:
        bold;

}}


.footer {{

    text-align:
        center;

    padding:
        30px;

    color:
        #64748b;

}}


@media(max-width: 1200px) {{

    .cards {{

        grid-template-columns:
            repeat(3, 1fr);

    }}

}}


@media(max-width: 800px) {{

    .cards {{

        grid-template-columns:
            repeat(2, 1fr);

    }}

    .grid {{

        grid-template-columns:
            1fr;

    }}

    .info-grid {{

        grid-template-columns:
            1fr;

    }}

}}


</style>

</head>


<body>


<div class="header">

    <h1>
        YOLO Video Analytics Dashboard
    </h1>

    <p>
        Computer Vision Object Detection,
        Tracking & Line-Crossing Analytics
    </p>

</div>


<div class="container">


<!-- ===================================== -->
<!-- KPI CARDS -->
<!-- ===================================== -->

<div class="cards">


    <div class="card">

        <div class="card-title">
            UNIQUE OBJECTS
        </div>

        <div class="card-value blue">
            {unique_objects}
        </div>

    </div>


    <div class="card">

        <div class="card-title">
            CURRENT OBJECTS
        </div>

        <div class="card-value">
            {current_objects}
        </div>

    </div>


    <div class="card">

        <div class="card-title">
            ENTERED
        </div>

        <div class="card-value green">
            {entered}
        </div>

    </div>


    <div class="card">

        <div class="card-title">
            EXITED
        </div>

        <div class="card-value red">
            {exited}
        </div>

    </div>


    <div class="card">

        <div class="card-title">
            CROSSINGS
        </div>

        <div class="card-value yellow">
            {total_crossings}
        </div>

    </div>


    <div class="card">

        <div class="card-title">
            NET COUNT
        </div>

        <div class="card-value">
            {net_count}
        </div>

    </div>


</div>


<!-- ===================================== -->
<!-- CHARTS -->
<!-- ===================================== -->

<div class="grid">


    <div class="panel">

        <h2>
            Objects by Class
        </h2>

        <div class="chart-container">

            <canvas id="classChart"></canvas>

        </div>

    </div>


    <div class="panel">

        <h2>
            Detections by Class
        </h2>

        <div class="chart-container">

            <canvas id="detectionChart"></canvas>

        </div>

    </div>


</div>


<!-- ===================================== -->
<!-- CLASS STATISTICS -->
<!-- ===================================== -->

<div class="panel">

    <h2>
        Class Analytics
    </h2>

    <table>

        <thead>

            <tr>

                <th>
                    Class
                </th>

                <th>
                    Unique Objects
                </th>

                <th>
                    Detections
                </th>

                <th>
                    Entered
                </th>

                <th>
                    Exited
                </th>

            </tr>

        </thead>

        <tbody>

            {class_rows}

        </tbody>

    </table>

</div>


<br>


<!-- ===================================== -->
<!-- VIDEO INFORMATION -->
<!-- ===================================== -->

<div class="panel">

    <h2>
        Video Information
    </h2>


    <div class="info-grid">


        <div class="info-box">

            <div class="info-label">
                Resolution
            </div>

            <div class="info-value">
                {video_width} × {video_height}
            </div>

        </div>


        <div class="info-box">

            <div class="info-label">
                Video FPS
            </div>

            <div class="info-value">
                {video_fps:.2f}
            </div>

        </div>


        <div class="info-box">

            <div class="info-label">
                Duration
            </div>

            <div class="info-value">
                {duration:.2f} seconds
            </div>

        </div>


        <div class="info-box">

            <div class="info-label">
                Total Frames
            </div>

            <div class="info-value">
                {total_frames}
            </div>

        </div>


        <div class="info-box">

            <div class="info-label">
                Frames Processed
            </div>

            <div class="info-value">
                {frames_processed}
            </div>

        </div>


        <div class="info-box">

            <div class="info-label">
                Processing FPS
            </div>

            <div class="info-value">
                {processing_fps:.2f}
            </div>

        </div>


        <div class="info-box">

            <div class="info-label">
                Processing Time
            </div>

            <div class="info-value">
                {processing_time:.2f} seconds
            </div>

        </div>


        <div class="info-box">

            <div class="info-label">
                Confidence
            </div>

            <div class="info-value">
                {confidence:.2f}
            </div>

        </div>


        <div class="info-box">

            <div class="info-label">
                IoU
            </div>

            <div class="info-value">
                {iou:.2f}
            </div>

        </div>


        <div class="info-box">

            <div class="info-label">
                Tracker
            </div>

            <div class="info-value">
                {tracker}
            </div>

        </div>


        <div class="info-box">

            <div class="info-label">
                Model
            </div>

            <div class="info-value">
                {model_path}
            </div>

        </div>


    </div>

</div>


<br>


<!-- ===================================== -->
<!-- TRACK DETAILS -->
<!-- ===================================== -->

<div class="panel">

    <h2>
        Object Tracking Details
    </h2>

    <table>

        <thead>

            <tr>

                <th>
                    Track ID
                </th>

                <th>
                    Class
                </th>

                <th>
                    First Frame
                </th>

                <th>
                    Last Frame
                </th>

                <th>
                    Frames Tracked
                </th>

                <th>
                    Max Confidence
                </th>

                <th>
                    Entry
                </th>

                <th>
                    Exit
                </th>

                <th>
                    Direction
                </th>

            </tr>

        </thead>

        <tbody>

            {track_rows}

        </tbody>

    </table>

</div>


</div>


<div class="footer">

    YOLO Video Analytics |
    Computer Vision Project

</div>


<script>


// ==========================================
// OBJECTS BY CLASS CHART
// ==========================================

const classCtx =
    document
    .getElementById(
        "classChart"
    )
    .getContext("2d");


new Chart(
    classCtx,
    {{

        type:
            "bar",

        data:
        {{

            labels:
                {json.dumps(class_labels)},

            datasets:
            [{{

                label:
                    "Unique Objects",

                data:
                    {json.dumps(class_values)},

                backgroundColor:
                    "#38bdf8"

            }}]

        }},

        options:
        {{

            responsive:
                true,

            maintainAspectRatio:
                false,

            plugins:
            {{

                legend:
                {{

                    labels:
                    {{

                        color:
                            "#e2e8f0"

                    }}

                }}

            }},

            scales:
            {{

                x:
                {{

                    ticks:
                    {{

                        color:
                            "#94a3b8"

                    }}

                }},

                y:
                {{

                    beginAtZero:
                        true,

                    ticks:
                    {{

                        color:
                            "#94a3b8"

                    }}

                }}

            }}

        }}

    }}
);


// ==========================================
// DETECTIONS BY CLASS CHART
// ==========================================

const detectionCtx =
    document
    .getElementById(
        "detectionChart"
    )
    .getContext("2d");


new Chart(
    detectionCtx,
    {{

        type:
            "doughnut",

        data:
        {{

            labels:
                {json.dumps(class_detection_labels)},

            datasets:
            [{{

                label:
                    "Detections",

                data:
                    {json.dumps(class_detection_values)},

                backgroundColor:
                [
                    "#38bdf8",
                    "#22c55e",
                    "#facc15",
                    "#ef4444",
                    "#a78bfa",
                    "#fb7185",
                    "#2dd4bf",
                    "#f97316"
                ]

            }}]

        }},

        options:
        {{

            responsive:
                true,

            maintainAspectRatio:
                false,

            plugins:
            {{

                legend:
                {{

                    position:
                        "bottom",

                    labels:
                    {{

                        color:
                            "#e2e8f0"

                    }}

                }}

            }}

        }}

    }}
);


</script>


</body>

</html>
"""


# ==========================================
# SAVE DASHBOARD
# ==========================================

with open(

    OUTPUT_HTML,

    "w",

    encoding="utf-8"

) as file:

    file.write(html)


# ==========================================
# TERMINAL SUMMARY
# ==========================================

print("\n========================================")

print(
    "ANALYTICS DASHBOARD GENERATED"
)

print("========================================")

print(
    f"Total detections: "
    f"{sum(detections_by_class.values())}"
)

print(
    f"Unique objects: "
    f"{unique_objects}"
)

print(
    f"Entered: "
    f"{entered}"
)

print(
    f"Exited: "
    f"{exited}"
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
    f"Dashboard saved to: "
    f"{OUTPUT_HTML}"
)

print("========================================")


# ==========================================
# OPEN DASHBOARD
# ==========================================

webbrowser.open(
    os.path.abspath(
        OUTPUT_HTML
    )
)