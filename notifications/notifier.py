from notifications.telegram_bot import TelegramBot
from notifications.email_notifier import EmailNotifier

class Notifier:
    def __init__(self):
        self.telegram_bot = TelegramBot()
        self.email_notifier = EmailNotifier(
            smtp_server="smtp.gmail.com",  # یا سرور SMTP دیگر
            smtp_port=587,
            sender_email="your_email@gmail.com",
            sender_password="your_email_password"
        )

    def send_telegram_message(self, message):
        self.telegram_bot.send_message(message)

    def send_email(self, recipient_email, subject, body):
        self.email_notifier.send_email(recipient_email, subject, body)