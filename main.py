from core.repo_scanner import scan_and_push
from config.settings import REPOS_FILE
from utils.notifier import Notifier

if __name__ == "__main__":
    notifier = Notifier()
    try:
        scan_and_push(REPOS_FILE)
        notifier.send_telegram_message("Repositories scanned and pushed successfully!")
    except Exception as e:
        notifier.send_telegram_message(f"An error occurred: {e}")