import os
import requests
from datetime import datetime


def get_log_path():
    if os.geteuid() == 0:  # Check if running as root
        return "/var/log/auto_git_pusher.log"
    else:
        user_log_dir = os.path.expanduser("~/.local/share/auto_git_pusher/logs")
        os.makedirs(user_log_dir, exist_ok=True)
        return os.path.join(user_log_dir, "run.log")

LOG_FILE = get_log_path()

def log(message):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted = f"[{now}] {message}"
    print(formatted)
    with open(LOG_FILE, "a") as f:
        f.write(formatted + "\n")
    # Send the log message to Telegram