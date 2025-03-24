# main.py - WiFi-Protect Ultra Orchestrator

import time
import threading
from modules.device_scanner import scan_devices
from modules.logger import log_event
from modules.notifier import notify_desktop, notify_telegram
from modules.rule_engine import evaluate_device
from modules.panic import trigger_panic_mode
from modules.geo_locator import get_location
from modules.honeypot import start_honeypot
from modules.dashboard import launch_dashboard
from modules.ghost_mode import ghost_log

# ✅ Configuration
TRUSTED_MACS = {
    "6C:94:66:35:EF:A8": "My Laptop",
    "11:22:33:44:55:66": "My Phone",
    "AA:BB:CC:DD:EE:FF": "PlayStation"
}

CHECK_INTERVAL = 60  # Check every 60 seconds

# 🚀 Startup Banner
def display_banner():
    banner = r"""
██╗    ██╗██╗███████╗██╗     ███████╗    ██████╗ ██████╗  ██████╗███████╗████████╗
██║    ██║██║██╔════╝██║     ██╔════╝    ██╔══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝
██║ █╗ ██║██║█████╗  ██║     █████╗      ██████╔╝██████╔╝██║     █████╗     ██║   
██║███╗██║██║██╔══╝  ██║     ██╔══╝      ██╔═══╝ ██╔═══╝ ██║     ██╔══╝     ██║   
╚███╔███╔╝██║██║     ██     ╗███████╗    ██║     ██║     ╚██████╗███████╗   ██║   
 ╚══╝╚══╝ ╚═╝╚═╝     ╚══════╝╚══════╝    ╚═╝     ╚═╝      ╚═════╝╚══════╝   ╚═╝   
                                                
                      🚀 WiFi-Protect Ultra 🚀    
             Advanced WiFi Security & Monitoring System
      This tool is powered by XKemoz | Italian.Kareem
📌 Facebook: https://www.facebook.com/Italian.Kareem/
📌 GitHub  : https://github.com/xkemoz
"""
    print(banner)

# 🔍 Device Monitoring
def monitor():
    known = set(TRUSTED_MACS.keys())
    while True:
        connected = scan_devices()
        new_devices = [d for d in connected if d['mac'] not in known]

        for device in new_devices:
            score = evaluate_device(device)
            loc = get_location(device.get('ip', '0.0.0.0'))
            device['location'] = loc

            log_event(device)
            ghost_log(device)

            if score >= 10:
                notify_telegram("⚠️ Suspicious device detected!", str(device))
                notify_desktop("Unknown Device", f"{device['mac']} from {loc}")
                trigger_panic_mode(device)
                start_honeypot()

        time.sleep(CHECK_INTERVAL)

# 🚀 Program Execution
if __name__ == '__main__':
    display_banner()
    print("🛰️ Starting WiFi-Protect Ultra...")
    threading.Thread(target=launch_dashboard).start()
    monitor()
