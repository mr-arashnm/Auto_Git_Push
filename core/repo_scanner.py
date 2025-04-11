import os
from core.git_handler import handle_git_repo
from utils.logger import log


def scan_and_push(repos_file):
    if not os.path.isfile(repos_file):
        log(f"❌ File not found: {repos_file}")
        return

    with open(repos_file, "r") as f:
        repos = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    if not repos:
        log("⚠️ Warning: The repos.txt file is empty (only comments or blank lines). Please add your git repositories.")
        # Optionally reset the file with sample content
        with open(repos_file, "w") as f:
            f.write("# Add your git repositories here\n")
            f.write("# Example: /path/to/your/repo\n")
        return
    
    for repo in repos:
        if os.path.isdir(os.path.join(repo, ".git")):
            handle_git_repo(repo)
        else:
            log(f"⚠️ Not a git repo: {repo}")
