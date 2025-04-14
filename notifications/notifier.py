from notifications.telegram_bot import TelegramBot
from notifications.email_notifier import EmailNotifier
from config.settings import EMAIL_NOTIFICATIONS_ENABLED
from config.settings import TELEGRAM_NOTIFICATIONS_ENABLED

class Notifier:
    def __init__(self):
        self.telegram_bot = TelegramBot()
        self.email_notifier = EmailNotifier()

    def notify(self, message, send_to=["telegram", "email"], email_recipient=None, email_subject=None):
        if "telegram" in send_to:
            if TELEGRAM_NOTIFICATIONS_ENABLED:  # بررسی وضعیت نوتیفیکیشن تلگرام
                self.telegram_bot.send_message(message)
            else:
                print("Telegram notifications are disabled. Skipping telegram notification.")

        if "email" in send_to and email_recipient:
            if EMAIL_NOTIFICATIONS_ENABLED:  # بررسی وضعیت نوتیفیکیشن ایمیل
                self.email_notifier.send_email(
                    recipient_email=email_recipient,
                    subject=email_subject or "Notification",
                    body=message
                )
            else:
                print("Email notifications are disabled. Skipping email.")