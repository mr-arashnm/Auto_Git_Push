import requests
import base64
from config.secure_settings import ENCODED_BOT_TOKEN, ENCODED_CHAT_ID

class Notifier:
    def __init__(self):
        # رمزگشایی مقادیر
        self.bot_token = base64.b64decode(ENCODED_BOT_TOKEN).decode("utf-8")
        self.chat_id = base64.b64decode(ENCODED_CHAT_ID).decode("utf-8")

    def send_telegram_message(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Raise an error for bad responses
            print("Telegram notification sent successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send Telegram notification: {e}")