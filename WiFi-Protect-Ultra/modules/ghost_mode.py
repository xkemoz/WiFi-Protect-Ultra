import json
import os
import time

# Storage file name
GHOST_LOG_FILE = "logs/ghost_log.json"

# Create the log file if it does not exist
if not os.path.exists(GHOST_LOG_FILE):
    with open(GHOST_LOG_FILE, "w") as f:
        json.dump([], f)

def ghost_log(device):
    """ Logs unknown devices in ghost mode without printing any notifications """
    try:
        # Read the current log
        with open(GHOST_LOG_FILE, "r") as f:
            logs = json.load(f)

        # Add the new device with a timestamp
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ip": device.get("ip", "Unknown"),
            "mac": device.get("mac", "Unknown"),
            "vendor": device.get("vendor", "Unknown")
        }
        logs.append(entry)

        # Save the updated log file
        with open(GHOST_LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"[GHOST MODE ERROR] Failed to log device: {e}")
