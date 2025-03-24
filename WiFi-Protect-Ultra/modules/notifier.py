import requests
from plyer import notification

# 🔹 Telegram Settings
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your actual token
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"  # Replace with your actual Chat ID

def notify_desktop(title, message):
    """ Send a desktop notification """
    try:
        notification.notify(title=title, message=message, timeout=5)
        print(f"✅ [NOTIFIER] Desktop Notification Sent: {title} - {message}")
    except Exception as e:
        print(f"❌ [NOTIFIER ERROR] Failed to send desktop notification: {e}")

def notify_telegram(title, message):
    """ Send a notification to Telegram """
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": f"📢 {title}\n\n{message}"}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print(f"✅ [NOTIFIER] Telegram Message Sent: {title}")
        else:
            print(f"❌ [NOTIFIER ERROR] Failed to send Telegram message: {response.text}")
    
    except Exception as e:
        print(f"❌ [NOTIFIER ERROR] {e}")
