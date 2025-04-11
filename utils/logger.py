import os
import requests
from datetime import datetime
import base64
from config.secure_settings import ENCODED_BOT_TOKEN, ENCODED_CHAT_ID

def get_log_path():
    if os.geteuid() == 0:  # Check if running as root
        return "/var/log/auto_git_pusher.log"
    else:
        user_log_dir = os.path.expanduser("~/.local/share/auto_git_pusher/logs")
        os.makedirs(user_log_dir, exist_ok=True)
        return os.path.join(user_log_dir, "run.log")

LOG_FILE = get_log_path()

# رمزگشایی مقادیر
TELEGRAM_BOT_TOKEN = base64.b64decode(ENCODED_BOT_TOKEN).decode("utf-8")
TELEGRAM_CHAT_ID = base64.b64decode(ENCODED_CHAT_ID).decode("utf-8")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        print("Telegram notification sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram notification: {e}")

def log(message):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted = f"[{now}] {message}"
    print(formatted)
    with open(LOG_FILE, "a") as f:
        f.write(formatted + "\n")
    # Send the log message to Telegram
    send_telegram_message(formatted)