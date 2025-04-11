import requests

def get_chat_id(telegram_bot_token, telegram_user_id):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/getUpdates"
    
    # Send request to Telegram to get updates
    response = requests.get(url)
    
    if response.status_code == 200:
        updates = response.json()['result']
        
        # Search for chat ID based on user_id
        for update in updates:
            if 'message' in update:
                message = update['message']
                if 'from' in message and message['from']['id'] == telegram_user_id:
                    chat_id = message['chat']['id']
                    return chat_id
        return None
    else:
        print("Error fetching updates.")
        return None

# Example usage of the function
telegram_bot_token = "Enter your Telegram bot token here"
telegram_user_id = "Enter the user ID of the desired Telegram user"

chat_id = get_chat_id(telegram_bot_token, telegram_user_id)
if chat_id:
    print(f"User's chat ID: {chat_id}")
else:
    print("Chat ID not found.")
