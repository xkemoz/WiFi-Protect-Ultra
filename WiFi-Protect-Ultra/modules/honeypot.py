import socket
import threading
import json
import os
import time

HONEYPOT_LOG_FILE = "logs/honeypot_log.json"
HONEYPOT_PORTS = [21, 22, 23, 80, 443, 3389]  # FTP, SSH, Telnet, HTTP, HTTPS, RDP

# Ensure the log file exists
if not os.path.exists(HONEYPOT_LOG_FILE):
    with open(HONEYPOT_LOG_FILE, "w") as f:
        json.dump([], f)

def log_intrusion(client_ip, port):
    """ Log an unauthorized connection attempt to the honeypot """
    try:
        with open(HONEYPOT_LOG_FILE, "r") as f:
            logs = json.load(f)

        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ip": client_ip,
            "port": port
        }
        logs.append(entry)

        with open(HONEYPOT_LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

        print(f"⚠️ [HONEYPOT ALERT] Intruder detected from {client_ip} on port {port}")

    except Exception as e:
        print(f"[HONEYPOT ERROR] Failed to log intrusion: {e}")

def honeypot_server(port):
    """ Run a Honeypot server on a specific port """
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", port))
        server.listen(5)
        print(f"[HONEYPOT] Listening on port {port}...")

        while True:
            client, addr = server.accept()
            log_intrusion(addr[0], port)
            client.close()

    except Exception as e:
        print(f"[HONEYPOT ERROR] {e}")

def start_honeypot():
    """ Start the Honeypot on multiple ports """
    print("[HONEYPOT] Activated")
    for port in HONEYPOT_PORTS:
        threading.Thread(target=honeypot_server, args=(port,), daemon=True).start()
