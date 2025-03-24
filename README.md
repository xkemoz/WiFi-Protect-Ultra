WiFi-Protect Ultra - Requirements & Usage Guide

 WiFi-Protect Ultra is an advanced WiFi security and monitoring tool that scans, detects, and protects your network from unauthorized devices and potential threats.
 Requirements (Dependencies)

Before running WiFi-Protect Ultra, ensure that you have installed the required dependencies.
 System Requirements

 Operating System: Linux-based (Recommended: Kali Linux, Parrot OS, Ubuntu, Arch)
Python Version: Python 3.8+
 Root Access: Required for scanning and network blocking features
 Required Packages

To install all dependencies, run this command in the project directory:

pip install -r requirements.txt

Alternatively, you can install them manually:

pip install flask requests pygame plyer geoip2

3️⃣ External Dependencies

✅ Nmap (For scanning devices)
Install it using:

sudo apt install nmap -y  # Debian-based
sudo pacman -S nmap       # Arch-based

GeoIP Database (For location tracking)
Download and extract:

mkdir -p /usr/share/GeoIP
wget -O /usr/share/GeoIP/GeoLite2-City.mmdb https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb

 iptables (For blocking malicious devices)
Pre-installed on most Linux systems. To install it manually:

sudo apt install iptables -y

nmcli (For WiFi management - Optional)

sudo apt install network-manager -y

How to Use WiFi-Protect Ultra?

This tool continuously monitors, logs, and protects your WiFi network.
 Clone the Repository

git clone https://github.com/xkemoz/WiFi-Protect-Ultra.git
cd WiFi-Protect-Ultra

 Install Dependencies

pip install -r requirements.txt

 Run the Tool

sudo python3 main.py

 Features and How They Work
Feature	Description
🔍 Real-time Device Scanning	Detects all devices connected to the network using Nmap.
 Ghost Mode	Logs suspicious devices without sending alerts.
 Panic Mode	Blocks intruders, triggers an alarm, and notifies the user.
Honeypot	Creates fake open ports to trap hackers and log their activity.
 GeoIP Tracking	Detects approximate locations of detected devices.
 Web Dashboard	Provides a web interface for monitoring activity (Flask-powered).
 Additional Commands
View Detected Devices (From Log)

cat logs/event_log.json

Manually Block a Device

sudo iptables -A INPUT -s 192.168.1.10 -j DROP
sudo iptables -A OUTPUT -d 192.168.1.10 -j DROP

Disable WiFi (Extreme Security Mode)

sudo nmcli radio wifi off

Enable WiFi Again

sudo nmcli radio wifi on

 How Does the Tool Work?

 Scans the local network using Nmap
 Detects new & suspicious devices based on risk scoring
 Logs all detected devices in logs/event_log.json
 If a high-risk device is found:

    ✅ Sends a desktop alert

    ✅ Sends a Telegram notification

    ✅ Blocks the device from accessing the network

    ✅ Triggers an alarm

    ✅ Starts a honeypot to lure attackers 5️⃣ Provides a Flask-powered dashboard to monitor live activity

Credits
🛠 Developed by XKemoz
 Facebook: Italian.Kareem
 GitHub: xkemoz

Enjoy Ultimate WiFi Security with WiFi-Protect Ultra! 
