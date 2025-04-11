from core.repo_scanner import scan_and_push
from config.settings import REPOS_FILE

if __name__ == "__main__":
    scan_and_push(REPOS_FILE)
