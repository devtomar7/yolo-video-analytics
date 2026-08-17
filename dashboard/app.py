from flask import Flask, render_template, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = os.path.join(BASE_DIR, "output")

JSON_REPORT = os.path.join(
    OUTPUT_DIR,
    "analytics_summary.json"
)

VIDEO_FILE = "analytics_video.mp4"


@app.route("/")
def dashboard():

    return render_template("index.html")


@app.route("/api/analytics")
def analytics():

    if not os.path.exists(JSON_REPORT):

        return jsonify({
            "error": "Analytics report not found. Run main.py first."
        }), 404

    with open(
        JSON_REPORT,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return jsonify(data)


@app.route("/video")
def video():

    return send_from_directory(
        OUTPUT_DIR,
        VIDEO_FILE
    )


if __name__ == "__main__":

    print("========================================")
    print("YOLO VIDEO ANALYTICS DASHBOARD")
    print("========================================")
    print("Dashboard: http://127.0.0.1:5000")
    print("========================================")

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )