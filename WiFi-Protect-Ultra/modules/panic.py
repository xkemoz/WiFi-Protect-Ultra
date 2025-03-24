import os
import json
import time
import pygame
from modules.notifier import notify_desktop, notify_telegram

PANIC_LOG_FILE = "logs/panic_log.json"

# Alarm sound configuration
ALARM_SOUND = "media/alarm.mp3"

# Ensure the log file exists
if not os.path.exists(PANIC_LOG_FILE):
    with open(PANIC_LOG_FILE, "w") as f:
        json.dump([], f)

def log_panic(device):
    """ Log the device that triggered the emergency mode """
    try:
        with open(PANIC_LOG_FILE, "r") as f:
            logs = json.load(f)

        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ip": device.get("ip", "Unknown"),
            "mac": device.get("mac", "Unknown"),
            "vendor": device.get("vendor", "Unknown"),
            "reason": "Triggered Panic Mode"
        }
        logs.append(entry)

        with open(PANIC_LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

        print(f"⚠️ [PANIC] Logged device: {device}")

    except Exception as e:
        print(f"❌ [PANIC ERROR] Failed to log panic event: {e}")

def trigger_panic_mode(device):
    """ Activate emergency mode when a high-level threat is detected """
    print(f"🚨 [PANIC] Triggered for {device['mac']}")

    # Play alarm sound
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(ALARM_SOUND)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"❌ [PANIC ERROR] Failed to play alarm sound: {e}")

    # Send emergency notifications
    notify_desktop("🚨 PANIC MODE!", f"🔴 Suspicious device detected: {device['mac']}")
    notify_telegram("🚨 PANIC MODE!", f"🔴 Suspicious device detected: {device['mac']} - IP: {device['ip']}")

    # Log the device in the panic log
    log_panic(device)

    # Execute blocking commands
    os.system(f"sudo iptables -A INPUT -s {device['ip']} -j DROP")
    os.system(f"sudo iptables -A OUTPUT -d {device['ip']} -j DROP")
    print(f"⛔ [PANIC] Blocked {device['ip']} from the network!")

    # Optionally: Disable WiFi completely
    # os.system("nmcli radio wifi off")
