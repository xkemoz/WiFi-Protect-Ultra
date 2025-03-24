import json
import os
import time

LOG_FILE = "logs/event_log.json"

# Ensure the log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

def log_event(device):
    """ Logs all new devices in a JSON file """
    try:
        # Read the current log
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)

        # Create a new log entry
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ip": device.get("ip", "Unknown"),
            "mac": device.get("mac", "Unknown"),
            "vendor": device.get("vendor", "Unknown"),
            "status": "new_connection"
        }
        logs.append(entry)

        # Update the log file
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

        print(f"[LOG] New Device Logged: {device}")

    except Exception as e:
        print(f"[LOG ERROR] Failed to log device: {e}")
