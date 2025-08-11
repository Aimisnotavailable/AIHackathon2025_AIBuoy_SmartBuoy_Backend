
from datetime import datetime
import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
buoy_bp = Blueprint('buoy', __name__, url_prefix='/')

current_buoy = {}

@buoy_bp.route("fetch_data", methods=["POST"])
def buoy_fetch_data():
    if request.method == "POST":
        global current_buoy
        current_buoy = json.loads(request.data)
    return ""

@buoy_bp.route("request_buoy", methods=["GET"])
def request_buoy():
    global current_buoy
    return json.dumps(current_buoy)

@buoy_bp.route("", methods=["GET"])
def buoy_request():
    return "HELLO NIGGER"


