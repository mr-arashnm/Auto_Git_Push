import os
import json
from utils.logger import log

REPOS_FILE = os.path.expanduser("~/.local/share/auto_git_pusher/repos.json")

def read_repo_config():
    """
    Read settings from the settings.json file.
    """
    if not os.path.exists(REPOS_FILE):
        log(f"❌ REPOS file not found: {REPOS_FILE}")
        return {}
    with open(REPOS_FILE, "r") as f:
        return json.load(f)

def write_repo_config(REPOS):
    """
    Write REPOS to the REPOS.json file.
    """
    with open(REPOS_FILE, "w") as f:
        json.dump(REPOS, f, indent=4)
    log(f"✅ REPOS saved to {REPOS_FILE}")