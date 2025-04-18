import subprocess
import os
from datetime import datetime
from utils.logger import log

def git_add(repo_path):
    """
    Execute the git add command to stage changes.
    """
    log(f"🔍 Adding changes in {repo_path}")
    os.chdir(repo_path)
    subprocess.run(["git", "add", "."], check=True)
    log(f"✅ Changes added in {repo_path}")

def git_commit(repo_path):
    """
    Execute the git commit command to commit changes.
    """
    log(f"🔍 Committing changes in {repo_path}")
    os.chdir(repo_path)
    msg = f"Auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(["git", "commit", "-m", msg], check=True)
    log(f"✅ Changes committed in {repo_path}")

def git_push(repo_path):
    """
    Execute the git push command to push changes to the remote repository.
    """
    log(f"🔍 Pushing changes in {repo_path}")
    os.chdir(repo_path)
    subprocess.run(["git", "push"], check=True)
    log(f"✅ Changes pushed in {repo_path}")

def handle_git_repo(repo_path, actions):
    """
    Manage the repository based on the specified actions.
    """
    log(f"🔍 Checking {repo_path}")
    os.chdir(repo_path)

    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if result.stdout.strip():
        if "add" in actions:
            git_add(repo_path)
        if "commit" in actions:
            git_commit(repo_path)
        if "push" in actions:
            git_push(repo_path)
    else:
        log(f"✔️ No changes: {repo_path}")