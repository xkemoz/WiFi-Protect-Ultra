from flask import Flask, render_template, jsonify
from modules.device_scanner import scan_devices
import threading
import time
import os

# Set the template directory
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates'))
app = Flask(__name__, template_folder=template_dir)

# Temporary storage for connected devices
connected_devices = []

def update_devices():
    """ Update the list of connected devices every 10 seconds """
    global connected_devices
    while True:
        connected_devices = scan_devices()
        time.sleep(10)  # Update every 10 seconds

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/devices')
def get_devices():
    return jsonify(connected_devices)

def launch_dashboard():
    """ Start the dashboard and begin updating device data """
    threading.Thread(target=update_devices, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=False)
