import json
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# YOLO VIDEO ANALYTICS - PROFESSIONAL STREAMLIT DASHBOARD
# ============================================================

st.set_page_config(
    page_title="YOLO Video Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

CSV_FILE = OUTPUT_DIR / "analytics_report.csv"
TIMESERIES_FILE = OUTPUT_DIR / "analytics_timeseries.csv"
JSON_FILE = OUTPUT_DIR / "analytics_summary.json"
VIDEO_FILE = OUTPUT_DIR / "analytics_video.mp4"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background-color: #11151d;
        border-right: 1px solid #252c38;
    }


    /* =========================
       HERO
       ========================= */

    .hero-box {
        background: linear-gradient(
            135deg,
            #111827 0%,
            #172033 100%
        );

        border: 1px solid #263247;
        border-radius: 16px;

        padding: 25px 30px;
        margin-bottom: 25px;

        box-shadow:
            0 8px 30px rgba(0, 0, 0, 0.25);
    }


    /* =========================
       METRIC CARDS
       ========================= */

    div[data-testid="stMetric"] {
        background-color: #151b26;

        border: 1px solid #263247;

        border-radius: 12px;

        padding: 15px;

        min-height: 105px;
    }


    div[data-testid="stMetricLabel"] {
        color: #aab4c3;
    }


    div[data-testid="stMetricValue"] {
        color: #ffffff;
    }


    /* =========================
       SECTION HEADINGS
       ========================= */

    .section-header {
        font-size: 1.25rem;
        font-weight: 700;

        color: #f3f4f6;

        margin-top: 25px;
        margin-bottom: 12px;
    }


    /* =========================
       STATUS BOXES
       ========================= */

    .status-info {
        background-color: #111f33;

        border: 1px solid #244b78;

        color: #93c5fd;

        border-radius: 10px;

        padding: 12px 15px;

        margin: 15px 0;
    }


    .status-success {
        background-color: #10261a;

        border: 1px solid #1f6b3b;

        color: #6ee7a2;

        border-radius: 10px;

        padding: 12px 15px;

        margin: 15px 0;
    }


    /* =========================
       INFO CARDS
       ========================= */

    .pipeline-card {
        background-color: #151b26;

        border: 1px solid #263247;

        border-radius: 12px;

        padding: 18px;

        min-height: 150px;
    }


    .pipeline-title {
        font-size: 1rem;

        font-weight: 700;

        color: #ffffff;

        margin-bottom: 8px;
    }


    .pipeline-text {
        color: #aab4c3;

        font-size: 0.9rem;

        line-height: 1.5;
    }


    /* =========================
       FOOTER
       ========================= */

    .footer {
        text-align: center;

        color: #6f7a8a;

        padding: 20px 0 5px 0;

        font-size: 0.85rem;
    }


    /* =========================
       DATAFRAME
       ========================= */

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }


    /* =========================
       BUTTONS
       ========================= */

    .stDownloadButton button {
        width: 100%;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default


def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def find_column(df, candidates):

    if df.empty:
        return None

    lookup = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    for candidate in candidates:

        key = candidate.strip().lower()

        if key in lookup:
            return lookup[key]

    return None


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    tracks = pd.DataFrame()
    timeseries = pd.DataFrame()
    summary = {}

    # -------------------------
    # TRACK CSV
    # -------------------------

    if CSV_FILE.exists():

        try:
            tracks = pd.read_csv(CSV_FILE)
        except Exception as e:
            st.error(f"Could not read analytics CSV: {e}")


    # -------------------------
    # TIME SERIES
    # -------------------------

    if TIMESERIES_FILE.exists():

        try:
            timeseries = pd.read_csv(TIMESERIES_FILE)
        except Exception as e:
            st.error(f"Could not read time-series CSV: {e}")


    # -------------------------
    # JSON SUMMARY
    # -------------------------

    if JSON_FILE.exists():

        try:

            with open(
                JSON_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                summary = json.load(file)

        except Exception as e:

            st.error(
                f"Could not read analytics summary: {e}"
            )

    return tracks, timeseries, summary


tracks, timeseries, summary = load_data()


# ============================================================
# VALIDATION
# ============================================================

if not CSV_FILE.exists() and not JSON_FILE.exists():

    st.error(
        "Analytics data not found.\n\n"
        "Run the following command first:\n\n"
        "`python main.py`"
    )

    st.stop()


# ============================================================
# SUMMARY DATA
# ============================================================

video_info = summary.get(
    "video",
    {}
)

analytics = summary.get(
    "analytics",
    {}
)

class_stats = summary.get(
    "class_statistics",
    {}
)

processing = summary.get(
    "processing",
    {})


# ============================================================
# BASIC ANALYTICS
# ============================================================

unique_objects = safe_int(
    analytics.get(
        "unique_objects",
        len(tracks)
    )
)


entered = safe_int(
    analytics.get(
        "entered",
        0
    )
)


exited = safe_int(
    analytics.get(
        "exited",
        0
    )
)


total_crossings = safe_int(
    analytics.get(
        "total_crossings",
        entered + exited
    )
)


net_count = safe_int(
    analytics.get(
        "net_count",
        entered - exited
    )
)


current_objects = safe_int(
    analytics.get(
        "current_objects",
        0
    )
)


# ============================================================
# PROCESSING INFORMATION
# ============================================================

average_fps = safe_float(
    processing.get(
        "average_processing_fps",
        0
    )
)


processing_time = safe_float(
    processing.get(
        "processing_time_seconds",
        0
    )
)


# ============================================================
# VIDEO INFORMATION
# ============================================================

width = safe_int(
    video_info.get(
        "width",
        0
    )
)


height = safe_int(
    video_info.get(
        "height",
        0
    )
)


video_fps = safe_float(
    video_info.get(
        "fps",
        0
    )
)


total_frames = safe_int(
    video_info.get(
        "total_frames",
        0
    )
)


duration = safe_float(
    video_info.get(
        "duration_seconds",
        0
    )
)


# ============================================================
# DETECTIONS BY CLASS
# ============================================================

detections_by_class = class_stats.get(
    "detections_by_class",
    {}
)


total_detections = sum(
    safe_int(value)
    for value in detections_by_class.values()
)


if total_detections == 0 and not tracks.empty:

    total_detections = len(tracks)


# ============================================================
# CURRENT OBJECTS FROM TIME SERIES
# ============================================================

if not timeseries.empty:

    possible_current_col = find_column(
        timeseries,
        [
            "Current Objects",
            "current_objects",
            "Current Objects Count",
            "objects"
        ]
    )

    if possible_current_col:

        series = pd.to_numeric(
            timeseries[possible_current_col],
            errors="coerce"
        ).dropna()

        if not series.empty:

            current_objects = int(
                series.iloc[-1]
            )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚙️ Dashboard Controls")

    st.caption(
        "YOLO11 + ByteTrack Video Analytics"
    )

    st.divider()

    st.subheader("Filters")


    # -------------------------
    # VEHICLE CLASS
    # -------------------------

    selected_class = "All"

    class_column = find_column(
        tracks,
        [
            "Class",
            "class"
        ]
    )


    if class_column and not tracks.empty:

        classes = sorted(
            tracks[class_column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_class = st.selectbox(
            "Vehicle Class",
            ["All"] + classes
        )


    # -------------------------
    # CONFIDENCE
    # -------------------------

    min_confidence = st.slider(
        "Minimum Confidence",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.05
    )


    # -------------------------
    # DIRECTION
    # -------------------------

    direction_options = [
        "All",
        "left_to_right",
        "right_to_left",
        "none"
    ]

    selected_direction = st.selectbox(
        "Direction",
        direction_options
    )


    st.divider()


    # -------------------------
    # PROJECT FILES
    # -------------------------

    st.subheader("Project Files")

    st.caption(
        "Files generated by main.py"
    )

    st.write(
        f"CSV Report: "
        f"{'✅ Available' if CSV_FILE.exists() else '❌ Missing'}"
    )

    st.write(
        f"JSON Summary: "
        f"{'✅ Available' if JSON_FILE.exists() else '❌ Missing'}"
    )

    st.write(
        f"Time-Series: "
        f"{'✅ Available' if TIMESERIES_FILE.exists() else '❌ Missing'}"
    )

    st.write(
        f"Processed Video: "
        f"{'✅ Available' if VIDEO_FILE.exists() else '❌ Missing'}"
    )


# ============================================================
# FILTER TRACK DATA
# ============================================================

filtered_tracks = tracks.copy()


if not filtered_tracks.empty:

    # -------------------------
    # CONFIDENCE FILTER
    # -------------------------

    confidence_column = find_column(
        filtered_tracks,
        [
            "Max Confidence",
            "max_confidence",
            "Confidence",
            "confidence"
        ]
    )


    if confidence_column:

        filtered_tracks["_confidence"] = pd.to_numeric(
            filtered_tracks[confidence_column],
            errors="coerce"
        ).fillna(0)

        filtered_tracks = filtered_tracks[
            filtered_tracks["_confidence"]
            >= min_confidence
        ]


    # -------------------------
    # CLASS FILTER
    # -------------------------

    if (
        class_column
        and selected_class != "All"
    ):

        filtered_tracks = filtered_tracks[
            filtered_tracks[class_column]
            .astype(str)
            == selected_class
        ]


    # -------------------------
    # DIRECTION FILTER
    # -------------------------

    direction_column = find_column(
        filtered_tracks,
        [
            "Direction",
            "direction"
        ]
    )


    if (
        direction_column
        and selected_direction != "All"
    ):

        filtered_tracks = filtered_tracks[
            filtered_tracks[direction_column]
            .astype(str)
            == selected_direction
        ]


# ============================================================
# HERO SECTION
# ============================================================

# IMPORTANT:
# Native Streamlit components are used here instead of raw HTML.
# This prevents <div> tags from appearing as text.

st.title(
    "🚗 YOLO Video Analytics Dashboard"
)

st.caption(
    "Computer Vision • Object Detection • "
    "Multi-Object Tracking • Line-Crossing Analytics"
)

st.info(
    "Production-style computer vision analytics dashboard "
    "powered by Ultralytics YOLO11, ByteTrack and OpenCV."
)


# ============================================================
# KPI SECTION
# ============================================================

st.subheader(
    "📊 Key Performance Indicators"
)


k1, k2, k3, k4, k5, k6 = st.columns(6)


with k1:

    st.metric(
        "Unique Objects",
        f"{unique_objects:,}"
    )


with k2:

    st.metric(
        "Total Detections",
        f"{total_detections:,}"
    )


with k3:

    st.metric(
        "Entered",
        f"{entered:,}"
    )


with k4:

    st.metric(
        "Exited",
        f"{exited:,}"
    )


with k5:

    st.metric(
        "Crossings",
        f"{total_crossings:,}"
    )


with k6:

    st.metric(
        "Net Count",
        f"{net_count:,}"
    )


# ============================================================
# CURRENT OBJECTS + STATUS
# ============================================================

st.subheader(
    "🚦 Current Scene Status"
)


s1, s2 = st.columns(2)


with s1:

    st.metric(
        "Current Objects",
        f"{current_objects:,}"
    )


with s2:

    if entered == 0 and exited == 0:

        st.info(
            "No line crossings were recorded in this video. "
            "Object detection and tracking are active."
        )

    else:

        st.success(
            "Line-crossing events detected successfully."
        )


# ============================================================
# VIDEO INFORMATION
# ============================================================

st.subheader(
    "🎥 Video & Processing Information"
)


v1, v2, v3, v4, v5, v6 = st.columns(6)


with v1:

    st.metric(
        "Resolution",
        f"{width} × {height}"
    )


with v2:

    st.metric(
        "Video FPS",
        f"{video_fps:.2f}"
    )


with v3:

    st.metric(
        "Frames",
        f"{total_frames:,}"
    )


with v4:

    st.metric(
        "Duration",
        f"{duration:.2f}s"
    )


with v5:

    st.metric(
        "Processing FPS",
        f"{average_fps:.2f}"
    )


with v6:

    st.metric(
        "Processing Time",
        f"{processing_time:.2f}s"
    )


# ============================================================
# PROCESSED VIDEO
# ============================================================

st.subheader(
    "▶️ Processed Video"
)


if VIDEO_FILE.exists():

    st.video(
        str(VIDEO_FILE)
    )

else:

    st.warning(
        "Processed video not found. "
        "Run `python main.py` first."
    )


# ============================================================
# VEHICLE CLASS DISTRIBUTION
# ============================================================

st.subheader(
    "🚘 Vehicle Class Distribution"
)


class_df = pd.DataFrame(
    list(
        detections_by_class.items()
    ),
    columns=[
        "Class",
        "Detections"
    ]
)


if not class_df.empty:

    class_df["Detections"] = pd.to_numeric(
        class_df["Detections"],
        errors="coerce"
    ).fillna(0).astype(int)


    c1, c2 = st.columns(
        [1.5, 1]
    )


    with c1:

        st.bar_chart(
            class_df.set_index("Class")
        )


    with c2:

        st.dataframe(
            class_df,
            width="stretch",
            hide_index=True
        )

else:

    st.info(
        "No vehicle class distribution data available."
    )


# ============================================================
# ENTRY / EXIT ANALYTICS
# ============================================================

st.subheader(
    "🔄 Entry / Exit Analytics"
)


entry_exit_df = pd.DataFrame(
    {
        "Metric": [
            "Entered",
            "Exited"
        ],
        "Count": [
            entered,
            exited
        ]
    }
)


e1, e2 = st.columns(
    [1.5, 1]
)


with e1:

    st.bar_chart(
        entry_exit_df.set_index("Metric")
    )


with e2:

    st.dataframe(
        entry_exit_df,
        width="stretch",
        hide_index=True
    )


# ============================================================
# ENTRY / EXIT BY CLASS
# ============================================================

entry_by_class = class_stats.get(
    "entered_by_class",
    {}
)


exit_by_class = class_stats.get(
    "exited_by_class",
    {}
)


entry_exit_classes = sorted(
    set(entry_by_class)
    | set(exit_by_class)
)


st.subheader(
    "🚦 Entry / Exit by Vehicle Class"
)


if entry_exit_classes:

    entry_exit_class_df = pd.DataFrame(
        {
            "Class": entry_exit_classes
        }
    )


    entry_exit_class_df["Entered"] = (
        entry_exit_class_df["Class"]
        .map(entry_by_class)
        .fillna(0)
        .astype(int)
    )


    entry_exit_class_df["Exited"] = (
        entry_exit_class_df["Class"]
        .map(exit_by_class)
        .fillna(0)
        .astype(int)
    )


    st.bar_chart(
        entry_exit_class_df.set_index(
            "Class"
        )[[
            "Entered",
            "Exited"
        ]]
    )


    st.dataframe(
        entry_exit_class_df,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No entry/exit events were recorded by vehicle class."
    )


# ============================================================
# TIME SERIES
# ============================================================

st.subheader(
    "📈 Time-Series Analytics"
)


if not timeseries.empty:

    ts = timeseries.copy()


    # -------------------------
    # FRAME COLUMN
    # -------------------------

    frame_col = find_column(
        ts,
        [
            "Frame",
            "frame",
            "Frame Number",
            "frame_number"
        ]
    )


    # -------------------------
    # TIME COLUMN
    # -------------------------

    time_col = find_column(
        ts,
        [
            "Video Time",
            "video_time",
            "Time",
            "time",
            "timestamp"
        ]
    )


    # -------------------------
    # CURRENT OBJECTS
    # -------------------------

    objects_col = find_column(
        ts,
        [
            "Current Objects",
            "current_objects",
            "Current Object Count",
            "objects"
        ]
    )


    # -------------------------
    # PROGRESS
    # -------------------------

    progress_col = find_column(
        ts,
        [
            "Progress",
            "progress"
        ]
    )


    # -------------------------
    # X AXIS
    # -------------------------

    if frame_col:

        ts["_frame"] = pd.to_numeric(
            ts[frame_col],
            errors="coerce"
        )

        x_axis = "_frame"

    elif time_col:

        ts["_time"] = pd.to_numeric(
            ts[time_col],
            errors="coerce"
        )

        x_axis = "_time"

    else:

        ts["_index"] = range(
            len(ts)
        )

        x_axis = "_index"


    chart_df = pd.DataFrame()


    # -------------------------
    # OBJECT COUNT
    # -------------------------

    if objects_col:

        chart_df["Current Objects"] = pd.to_numeric(
            ts[objects_col],
            errors="coerce"
        )


    # -------------------------
    # PROGRESS
    # -------------------------

    if progress_col:

        chart_df["Progress %"] = pd.to_numeric(
            ts[progress_col],
            errors="coerce"
        )


    if not chart_df.empty:

        chart_df.index = ts[x_axis]

        st.line_chart(
            chart_df
        )

        st.caption(
            "Time-series visualization generated from "
            "the analytics_timeseries.csv report."
        )

    else:

        st.info(
            "Time-series file exists, but no recognized "
            "numeric analytics columns were found."
        )

else:

    st.info(
        "Time-series report not found. "
        "Run `python main.py` to generate it."
    )


# ============================================================
# TRACK LEVEL ANALYTICS
# ============================================================

st.subheader(
    "🧾 Track-Level Analytics"
)


if not filtered_tracks.empty:

    display_df = filtered_tracks.copy()


    if "_confidence" in display_df.columns:

        display_df = display_df.drop(
            columns=[
                "_confidence"
            ]
        )


    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
        height=420
    )


    st.caption(
        f"Showing {len(display_df):,} tracked objects "
        "after applying filters."
    )

else:

    st.info(
        "No tracked objects match the selected filters."
    )


# ============================================================
# DOWNLOAD REPORTS
# ============================================================

st.subheader(
    "⬇️ Download Reports"
)


d1, d2, d3 = st.columns(3)


# -------------------------
# CSV
# -------------------------

if CSV_FILE.exists():

    with open(
        CSV_FILE,
        "rb"
    ) as file:

        csv_bytes = file.read()


    with d1:

        st.download_button(
            "⬇️ Download CSV Report",
            data=csv_bytes,
            file_name="analytics_report.csv",
            mime="text/csv",
            width="stretch"
        )


# -------------------------
# JSON
# -------------------------

if JSON_FILE.exists():

    with open(
        JSON_FILE,
        "rb"
    ) as file:

        json_bytes = file.read()


    with d2:

        st.download_button(
            "⬇️ Download JSON Summary",
            data=json_bytes,
            file_name="analytics_summary.json",
            mime="application/json",
            width="stretch"
        )


# -------------------------
# TIME SERIES CSV
# -------------------------

if TIMESERIES_FILE.exists():

    with open(
        TIMESERIES_FILE,
        "rb"
    ) as file:

        ts_bytes = file.read()


    with d3:

        st.download_button(
            "⬇️ Download Time-Series CSV",
            data=ts_bytes,
            file_name="analytics_timeseries.csv",
            mime="text/csv",
            width="stretch"
        )


# ============================================================
# COMPUTER VISION PIPELINE
# ============================================================

st.subheader(
    "🧠 Computer Vision Pipeline"
)


p1, p2, p3, p4 = st.columns(4)


with p1:

    st.info(
        "**Detection**\n\n"
        "YOLO11 detects vehicles and produces "
        "bounding boxes with confidence scores."
    )


with p2:

    st.info(
        "**Tracking**\n\n"
        "ByteTrack maintains object identities "
        "across video frames using persistent IDs."
    )


with p3:

    st.info(
        "**Line Crossing**\n\n"
        "Object center-point movement is compared "
        "with a vertical counting line."
    )


with p4:

    st.info(
        "**Analytics**\n\n"
        "CSV, JSON and time-series reports are "
        "generated for dashboard visualization."
    )


# ============================================================
# PROJECT TECHNOLOGY
# ============================================================

st.subheader(
    "🛠️ Technology Stack"
)


tech1, tech2, tech3, tech4, tech5 = st.columns(5)


with tech1:

    st.metric(
        "Detection",
        "YOLO11"
    )


with tech2:

    st.metric(
        "Tracking",
        "ByteTrack"
    )


with tech3:

    st.metric(
        "Vision",
        "OpenCV"
    )


with tech4:

    st.metric(
        "Dashboard",
        "Streamlit"
    )


with tech5:

    st.metric(
        "Analytics",
        "Pandas"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        YOLO Video Analytics • OpenCV • Ultralytics YOLO11 •
        ByteTrack • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)