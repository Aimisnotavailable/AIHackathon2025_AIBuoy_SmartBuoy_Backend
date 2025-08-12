
from datetime import datetime
import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file, Response
import threading
import time
import numpy as np
import cv2

# Shared storage for the latest frame bytes + a lock for thread-safety
frame_lock   = threading.Lock()
latest_frame = None  # will hold raw JPEG bytes
buoy_bp = Blueprint('buoy', __name__, url_prefix='/')

current_buoy = {}
frame_bytes = None

@buoy_bp.route("fetch_data", methods=["POST"])
def buoy_fetch_data():
    if request.method == "POST":
        global current_buoy
        current_buoy = json.loads(request.data)
    return ""

@buoy_bp.route("request_buoy", methods=["GET"])
def request_buoy():
    global current_buoy
    return current_buoy

@buoy_bp.route("", methods=["GET"])
def buoy_request():
    return "HELLO"

@buoy_bp.route("/capture_feed", methods=["POST"])
def capture_feed():
    global latest_frame

    data = request.get_json(force=True)
    # Extract the Latin-1–encoded string
    latin1_str = data["frame"]["data"]  

    # Reverse the Latin-1 mapping back to raw bytes
    raw_bytes = latin1_str.encode('latin-1')

    # (Optional) Sanity-check by decoding with OpenCV
    # import numpy as np
    # buf = np.frombuffer(raw_bytes, dtype=np.uint8)
    # img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    # if img is None:
    #     return ("Invalid frame data", 400)

    # Store the frame bytes in a thread-safe way
    with frame_lock:
        latest_frame = raw_bytes

    # Acknowledge
    return ("", 204)

def gen_mjpeg():
    global latest_frame

    while True:
        # Wait for a frame to arrive
        with frame_lock:
            frame = latest_frame

        if frame is None:
            time.sleep(0.01)
            continue

        # Build a single MJPEG part
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )

        # Throttle to ~24 FPS if needed
        time.sleep(0.04167)

@buoy_bp.route("live_feed", methods=["GET"])
def live_feed():
    return Response(
        gen_mjpeg(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )