# \# 🚗 YOLO Video Analytics

# 

# A computer vision video analytics system built using \*\*YOLO, OpenCV, ByteTrack, Python, Pandas, and Streamlit\*\* for vehicle detection, multi-object tracking, line-crossing analysis, and interactive analytics visualization.

# 

# The system processes video frames, detects and tracks vehicles, calculates object-level statistics, generates structured analytics reports, and provides an interactive dashboard for exploring the results.

# 

# \---

# 

# \# ✨ Features

# 

# \- 🎯 YOLO-based object detection

# \- 🆔 Multi-object tracking with ByteTrack

# \- 🚗 Vehicle-class analytics

# \- 📍 Persistent tracking IDs across frames

# \- 🚦 Line-crossing detection

# \- ↔️ Direction-based entry/exit analytics

# \- 📊 Class-wise detection statistics

# \- 📈 Time-series analytics

# \- 🎥 Processed video generation

# \- 🖥️ Interactive Streamlit dashboard

# \- 🔎 Vehicle-class filtering

# \- 🎚️ Minimum-confidence filtering

# \- ↔️ Direction filtering

# \- 📁 CSV analytics reports

# \- 📄 JSON summary reports

# \- ⬇️ Downloadable reports from the dashboard

# 

# \---

# 

# \# 🖼️ Project Screenshots

# 

# \## 🎯 YOLO Object Detection

# 

# The system detects vehicles in video frames using YOLO and displays bounding boxes, vehicle classes, confidence scores, and tracking information.

# 

# !\[YOLO Detection](screenshots/detection.png)

# 

# \---

# 

# \## 🖥️ Interactive Streamlit Dashboard

# 

# The Streamlit dashboard provides KPIs, filters, charts, video information, analytics, and downloadable reports.

# 

# !\[Streamlit Dashboard](screenshots/dashboard.png)

# 

# \---

# 

# \## 📊 Analytics Visualization

# 

# The analytics interface provides vehicle-class statistics, object counts, time-series information, and other insights generated from the processed video.

# 

# !\[Analytics Visualization](screenshots/analytics.png)

# 

# \---

# 

# \## 🆔 Multi-Object Tracking

# 

# ByteTrack maintains persistent tracking IDs across video frames, allowing the system to distinguish unique vehicles from repeated detections.

# 

# !\[Object Tracking](screenshots/tracking.png)

# 

# \---

# 

# \## 🎥 Processed Video

# 

# The system generates a processed video containing YOLO detection and tracking results.

# 

# !\[Processed Video](screenshots/video.png)

# 

# \---

# 

# \# 🧠 Computer Vision Pipeline

# 

# ```text

# Input Video

# &#x20;    │

# &#x20;    ▼

# OpenCV Video Capture

# &#x20;    │

# &#x20;    ▼

# YOLO Object Detection

# &#x20;    │

# &#x20;    ▼

# ByteTrack Multi-Object Tracking

# &#x20;    │

# &#x20;    ├── Track IDs

# &#x20;    ├── Vehicle Classes

# &#x20;    └── Confidence Scores

# &#x20;    │

# &#x20;    ▼

# Line-Crossing / Direction Analytics

# &#x20;    │

# &#x20;    ▼

# Analytics Engine

# &#x20;    │

# &#x20;    ├── CSV Report

# &#x20;    ├── JSON Summary

# &#x20;    └── Time-Series CSV

# &#x20;    │

# &#x20;    ▼

# Streamlit Dashboard

# ```

# 

# \---

# 

# \# 🛠️ Tech Stack

# 

# | Technology | Purpose |

# |---|---|

# | Python | Core application and analytics |

# | Ultralytics YOLO | Object detection |

# | ByteTrack | Multi-object tracking |

# | OpenCV | Video processing |

# | Pandas | Data processing and analytics |

# | NumPy | Numerical operations |

# | Streamlit | Interactive dashboard |

# | Matplotlib | Visualization |

# | CSV / JSON | Analytics report storage |

# | Git \& GitHub | Version control |

# 

# \---

# 

# \# 📂 Project Structure

# 

# ```text

# YOLO-OPEN-CV-VIDEO-ANALYTICS/

# │

# ├── dashboard/

# │   ├── app.py

# │   └── templates/

# │       └── index.html

# │

# ├── screenshots/

# │   ├── detection.png

# │   ├── dashboard.png

# │   ├── analytics.png

# │   ├── tracking.png

# │   └── video.png

# │

# ├── dashboard.py

# ├── dashboard\_app.py

# ├── main.py

# ├── main\_before\_dashboard\_integration.py

# ├── main\_before\_reporting\_backup.py

# ├── main\_class\_analytics\_backup.py

# ├── main\_tracking\_backup.py

# ├── requirements.txt

# ├── .gitignore

# └── README.md

# ```

# 

# \---

# 

# \# 🔧 Main Components

# 

# \### `main.py`

# 

# Runs the core video-processing pipeline, YOLO detection, tracking, line-crossing analytics, and report generation.

# 

# \### `dashboard\_app.py`

# 

# Provides the Streamlit dashboard with KPIs, filters, charts, track-level analytics, processed-video playback, and report downloads.

# 

# \### `dashboard.py`

# 

# Generates the analytics dashboard/report from the processed analytics data.

# 

# \---

# 

# \# 🚀 Installation

# 

# \## 1. Clone the Repository

# 

# ```bash

# git clone https://github.com/devtomar7/yolo-video-analytics.git

# cd yolo-video-analytics

# ```

# 

# \## 2. Create a Virtual Environment

# 

# \### Windows PowerShell

# 

# ```powershell

# python -m venv venv

# ```

# 

# Activate the virtual environment:

# 

# ```powershell

# .\\venv\\Scripts\\Activate.ps1

# ```

# 

# If PowerShell blocks script execution, run:

# 

# ```powershell

# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# ```

# 

# Then activate again:

# 

# ```powershell

# .\\venv\\Scripts\\Activate.ps1

# ```

# 

# \## 3. Install Dependencies

# 

# ```bash

# pip install -r requirements.txt

# ```

# 

# \---

# 

# \# ▶️ Usage

# 

# \## Run the Video Analytics Pipeline

# 

# ```bash

# python main.py

# ```

# 

# The pipeline generates analytics files including:

# 

# ```text

# output/

# ├── analytics\_report.csv

# ├── analytics\_timeseries.csv

# ├── analytics\_summary.json

# └── analytics\_video.mp4

# ```

# 

# \---

# 

# \## Generate the Dashboard

# 

# ```bash

# python dashboard.py

# ```

# 

# \---

# 

# \## Launch the Streamlit Dashboard

# 

# ```bash

# streamlit run dashboard\_app.py

# ```

# 

# The dashboard reads the analytics generated by `main.py`.

# 

# The application will normally be available at:

# 

# ```text

# http://localhost:8501

# ```

# 

# \---

# 

# \# 📊 Dashboard

# 

# The dashboard provides a production-style analytics interface with:

# 

# \## Key Performance Indicators

# 

# \- Unique Objects

# \- Total Detections

# \- Entered

# \- Exited

# \- Total Crossings

# \- Net Count

# 

# \## Video \& Processing Information

# 

# \- Resolution

# \- Video FPS

# \- Total frames

# \- Video duration

# \- Average processing FPS

# \- Processing time

# 

# \## Analytics

# 

# \- Vehicle-class distribution

# \- Entry/exit by vehicle class

# \- Time-series object counts

# \- Processing progress

# \- Track-level analytics

# \- Direction analysis

# 

# \## Filters

# 

# \- Vehicle class

# \- Minimum confidence

# \- Movement direction

# 

# \## Reports

# 

# Users can download:

# 

# ```text

# analytics\_report.csv

# analytics\_summary.json

# analytics\_timeseries.csv

# ```

# 

# \---

# 

# \# 🚦 Line-Crossing Analytics

# 

# The system tracks an object's movement relative to a configured counting line.

# 

# ```text

# &#x20;             COUNTING LINE

# &#x20;                   │

# &#x20;       🚗 ────────▶│

# &#x20;                   │

# &#x20;       ◀──────── 🚚│

# &#x20;                   │

# ```

# 

# Crossing events can be used to calculate:

# 

# \- Entry count

# \- Exit count

# \- Total crossings

# \- Net count

# \- Direction

# \- Entry/exit by vehicle class

# 

# \---

# 

# \# 🆔 Multi-Object Tracking

# 

# YOLO provides detections for each frame while ByteTrack associates detections across frames.

# 

# Example:

# 

# ```text

# Frame 1 → Car → Track ID 7

# Frame 2 → Car → Track ID 7

# Frame 3 → Car → Track ID 7

# Frame 4 → Car → Track ID 7

# ```

# 

# This allows the system to distinguish between repeated detections of the same vehicle and genuinely new objects.

# 

# \### Detection vs Tracking

# 

# ```text

# YOLO

# &#x20;↓

# "What objects are visible?"

# 

# ByteTrack

# &#x20;↓

# "Is this the same object I saw previously?"

# ```

# 

# \---

# 

# \# 📈 Time-Series Analytics

# 

# The dashboard visualizes time-series information generated by `main.py`, including:

# 

# \- Current object count

# \- Processing progress

# \- Frame progression

# \- Video-time progression

# 

# \---

# 

# \# 📁 Generated Reports

# 

# \## `analytics\_report.csv`

# 

# Track-level analytics used by the dashboard for filtering and inspection.

# 

# \## `analytics\_summary.json`

# 

# Structured summary containing:

# 

# \- Video metadata

# \- Object statistics

# \- Entry/exit counts

# \- Class statistics

# \- Processing information

# 

# \## `analytics\_timeseries.csv`

# 

# Frame/time-based analytics used for time-series visualization.

# 

# \## `analytics\_video.mp4`

# 

# Processed video containing detection and tracking results.

# 

# \---

# 

# \# 🧪 Example Test Run

# 

# A sample test run processed a \*\*1920 × 1080 video at 30 FPS with 90 frames\*\*.

# 

# ```text

# Total frames processed: 90

# Unique objects tracked: 18

# Objects entered: 0

# Objects exited: 0

# Total crossings: 0

# Net count: 0

# Final current objects: 7

# Average processing FPS: 5.56

# Processing time: 16.19 seconds

# ```

# 

# \## Unique Objects by Class

# 

# ```text

# car: 17

# truck: 1

# ```

# 

# \## Total Detections by Class

# 

# ```text

# car: 541

# truck: 45

# bus: 7

# ```

# 

# > Results depend on the input video, model configuration, confidence threshold, tracking behavior, and available hardware.

# 

# \---

# 

# \# 🔐 Git \& Data Handling

# 

# The project excludes large and generated files using `.gitignore`, including:

# 

# ```text

# venv/

# .venv/

# .env

# \_\_pycache\_\_/

# runs/

# \*.pt

# \*.onnx

# \*.mp4

# \*.avi

# \*.mov

# \*.mkv

# output/\*.csv

# output/\*.json

# output/\*.html

# ```

# 

# This keeps the GitHub repository focused on source code rather than large videos, model weights, generated reports, environment variables, and local environments.

# 

# \---

# 

# \# 💡 Engineering Highlights

# 

# This project demonstrates practical experience with:

# 

# \- Computer Vision

# \- Deep Learning inference

# \- Object detection

# \- Multi-object tracking

# \- Video processing

# \- Vehicle analytics

# \- Time-series analysis

# \- Data visualization

# \- Python

# \- Pandas

# \- Streamlit

# \- Git \& GitHub

# 

# The inference pipeline is separated from the analytics/dashboard layer, allowing previously generated results to be analyzed without rerunning the complete video-processing pipeline.

# 

# \---

# 

# \# 📌 Project Results

# 

# The tested pipeline successfully tracked:

# 

# ```text

# Unique Objects

# │

# ├── car: 17

# └── truck: 1

# ```

# 

# Total detections:

# 

# ```text

# Total Detections

# │

# ├── car: 541

# ├── truck: 45

# └── bus: 7

# ```

# 

# Generated analytics:

# 

# ```text

# ✓ Processed Video

# ✓ Track-Level CSV

# ✓ Time-Series CSV

# ✓ JSON Summary

# ✓ Interactive Streamlit Dashboard

# ```

# 

# \---

# 

# \# 🔮 Future Improvements

# 

# \- \[ ] Real-time webcam support

# \- \[ ] RTSP/IP camera support

# \- \[ ] GPU inference optimization

# \- \[ ] Configurable counting line through UI

# \- \[ ] Region-of-interest selection

# \- \[ ] Vehicle speed estimation

# \- \[ ] Traffic density estimation

# \- \[ ] Heatmap generation

# \- \[ ] Real-time alerts

# \- \[ ] Historical analytics database

# \- \[ ] Docker deployment

# \- \[ ] Cloud deployment

# \- \[ ] Authentication and multi-user dashboards

# 

# \---

# 

# \# 💼 Resume Description

# 

# \### YOLO Video Analytics | Python, YOLO, OpenCV, ByteTrack, Streamlit, Pandas

# 

# Developed a computer vision pipeline using YOLO and ByteTrack for vehicle detection and persistent multi-object tracking in video streams.

# 

# Implemented line-crossing and direction analytics to calculate unique objects, entries, exits, crossings, and class-wise detection statistics.

# 

# Built an interactive Streamlit analytics dashboard with KPI cards, vehicle-class filtering, confidence filtering, time-series visualization, processed-video playback, and downloadable reports.

# 

# Designed a structured analytics pipeline generating CSV, JSON, and time-series reports for track-level and video-level analysis.

# 

# \---

# 

# \# 👨‍💻 Author

# 

# \*\*Dev Tomar\*\*  

# B.Tech — Information Technology

# 

# GitHub: https://github.com/devtomar7

# 

# LinkedIn: https://linkedin.com/in/dev-tomar7

# 

# \---

# 

# \## ⭐ If you find this project useful, consider giving the repository a star.

# 

# \--- 

