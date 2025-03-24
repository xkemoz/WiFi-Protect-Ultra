import json
import os
import time

RISK_LOG_FILE = "logs/risk_log.json"

# Ensure the risk log file exists
if not os.path.exists(RISK_LOG_FILE):
    with open(RISK_LOG_FILE, "w") as f:
        json.dump({}, f)

def evaluate_device(device):
    """ Evaluate the risk level of a device based on its behavior """
    try:
        with open(RISK_LOG_FILE, "r") as f:
            risk_data = json.load(f)

        mac = device.get("mac", "Unknown")
        risk_score = 0

        # 🔹 1. Is the device new? (+5)
        if mac not in risk_data:
            risk_score += 5

        # 🔹 2. Is the device's IP changing frequently? (+3)
        if mac in risk_data and device["ip"] != risk_data[mac].get("last_ip", "0.0.0.0"):
            risk_score += 3

        # 🔹 3. Is the MAC address unknown or spoofed? (+7)
        if device["mac"] == "Unknown":
            risk_score += 7

        # 🔹 4. Has the device appeared in the Honeypot? (+10)
        if mac in risk_data and risk_data[mac].get("honeypot", False):
            risk_score += 10

        # 🔹 5. Has the device been detected in Ghost Mode? (+8)
        if mac in risk_data and risk_data[mac].get("ghost_detected", False):
            risk_score += 8

        # 🔹 6. Is the device stable in the network? (-10)
        if mac in risk_data and risk_data[mac].get("stable", False):
            risk_score -= 10

        # Update device information in the risk log
        risk_data[mac] = {
            "last_ip": device["ip"],
            "risk_score": risk_score,
            "last_seen": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(RISK_LOG_FILE, "w") as f:
            json.dump(risk_data, f, indent=4)

        print(f"🔍 [RULE ENGINE] Risk Score for {mac}: {risk_score}")

        return risk_score

    except Exception as e:
        print(f"❌ [RULE ENGINE ERROR] {e}")
        return 0
