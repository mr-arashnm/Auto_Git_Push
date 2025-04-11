import subprocess
import os
from datetime import datetime
from utils.logger import log

def handle_git_repo(repo_path):
    log(f"🔍 Checking {repo_path}")
    os.chdir(repo_path)

    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if result.stdout.strip():
        subprocess.run(["git", "add", "."], check=True)
        msg = f"Auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push"], check=True)
        log(f"✅ Pushed: {repo_path}")
    else:
        log(f"✔️ No changes: {repo_path}")
