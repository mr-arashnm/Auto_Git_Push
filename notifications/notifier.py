from notifications.telegram_bot import TelegramBot
from notifications.email_notifier import EmailNotifier


class Notifier:
    def __init__(self):
        self.telegram_bot = TelegramBot()
        self.email_notifier = EmailNotifier()

    def notify(self, message, send_to=["telegram", "email"], email_recipient=None, email_subject=None):

        if "telegram" in send_to:
            self.telegram_bot.send_message(message)

        if "email" in send_to and email_recipient:
            self.email_notifier.send_email(
                recipient_email=email_recipient,
                subject=email_subject or "Notification",
                body=message
            )