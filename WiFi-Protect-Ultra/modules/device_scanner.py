import subprocess
import re
import os

def scan_devices():
    """ Scan connected devices on the network using Nmap without the Nmap library """
    try:
        print("📡 Debug: Running Nmap scan...")

        # Ensure Nmap runs without issues
        if os.geteuid() != 0:
            print("⚠️ Debug: Running without root! Trying sudo...")
            return []

        # Run Nmap with sudo to scan the network
        result = subprocess.run(
            ["nmap", "-sn", "-e", "wlan0", "192.168.100.0/24"],  # Ensure wlan0 is the correct interface
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout

        # Print raw output for debugging
        print(f"📡 Debug: Raw Nmap Output:\n{output}")

        devices = []
        
        # Use regex to extract data
        ip_pattern = re.compile(r"Nmap scan report for (\d+\.\d+\.\d+\.\d+)")
        mac_pattern = re.compile(r"MAC Address: (\S+) \((.+)\)")

        ip_address = None
        for line in output.split("\n"):
            ip_match = ip_pattern.search(line)
            if ip_match:
                ip_address = ip_match.group(1)
                continue
            
            mac_match = mac_pattern.search(line)
            if mac_match and ip_address:
                mac_address = mac_match.group(1)
                vendor = mac_match.group(2)
                print(f"📡 Debug: Found Device - IP: {ip_address}, MAC: {mac_address}, Vendor: {vendor}")
                devices.append({"ip": ip_address, "mac": mac_address, "vendor": vendor})
                ip_address = None  # Reset IP for the next match

        print(f"✅ Debug: Scan completed. Found {len(devices)} devices.")
        return devices

    except subprocess.TimeoutExpired:
        print("❌ Debug: Nmap took too long to respond! Reducing scan range might help.")
        return []
    except Exception as e:
        print(f"❌ Debug: Error in scan_devices: {e}")
        return []

if __name__ == "__main__":
    scan_devices()
