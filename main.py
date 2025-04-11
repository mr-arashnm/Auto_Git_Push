from core.repo_scanner import scan_and_push
from config.settings import REPOS_FILE
from notifications.notifier import Notifier

if __name__ == "__main__":
    notifier = Notifier()
    try:
        scan_and_push(REPOS_FILE)
        notifier.notify(
            message="Repositories scanned and pushed successfully!",
            send_to=["telegram", "email"],  # ارسال به تلگرام و ایمیل
            email_recipient="arashnm797@gmail.com",
            email_subject="Repositories Update"
        )
    except Exception as e:
        notifier.notify(
            message=f"An error occurred: {e}",
            send_to=["telegram"],  # فقط ارسال به تلگرام
        )