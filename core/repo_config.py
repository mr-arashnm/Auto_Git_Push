import os
import json
from utils.logger import log

SETTINGS_FILE = os.path.expanduser("~/.local/share/auto_git_pusher/settings.json")

def read_repo_config():
    """
    Read settings from the settings.json file.
    """
    if not os.path.exists(SETTINGS_FILE):
        log(f"❌ Settings file not found: {SETTINGS_FILE}")
        return {}
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def write_repo_config(settings):
    """
    Write settings to the settings.json file.
    """
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
    log(f"✅ Settings saved to {SETTINGS_FILE}")