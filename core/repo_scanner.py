import os
from core.git_handler import handle_git_repo
from core.repo_config import read_settings
from utils.logger import log

def process_repositories():
    """
    Process all repositories based on the settings.
    """
    settings = read_settings()
    repositories = settings.get("repositories", [])

    for repo in repositories:
        repo_path = repo.get("path")
        actions = repo.get("actions", [])
        if not repo_path or not actions:
            log(f"⚠️ Invalid configuration for repository: {repo}")
            continue
        if os.path.isdir(os.path.join(repo_path, ".git")):
            handle_git_repo(repo_path, actions)
        else:
            log(f"⚠️ Not a git repository: {repo_path}")