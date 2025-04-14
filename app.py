from flask import Flask, request, jsonify, render_template
import os
from config.settings import REPOS_FILE, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, EMAIL_USERNAME
from utils.logger import log
from utils.validator import validate_repo_path

app = Flask(__name__)

# API برای دریافت تم
@app.route('/get-theme', methods=['GET'])
def get_theme():
    from config.settings import DEFAULT_THEME
    return jsonify({"theme": DEFAULT_THEME})

# API برای ذخیره تم
@app.route('/save-theme', methods=['POST'])
def save_theme():
    data = request.json
    theme = data.get('theme', 'light')  # پیش‌فرض: light

    # به‌روزرسانی فایل settings.py
    with open(os.path.expanduser("~/auto_git_pusher/config/settings.py"), "r") as f:
        lines = f.readlines()

    with open(os.path.expanduser("~/auto_git_pusher/config/settings.py"), "w") as f:
        for line in lines:
            if line.startswith("DEFAULT_THEME"):
                f.write(f'DEFAULT_THEME = "{theme}"\n')
            else:
                f.write(line)

    log(f"Theme updated to {theme}.")
    return jsonify({"message": "Theme updated successfully!"})

# API برای ولیدیت مسیرها
@app.route('/validate-path', methods=['POST'])
def validate_path():
    data = request.json
    path = data.get('path', '')
    is_valid = validate_repo_path(path)
    return jsonify({"isValid": is_valid})


# API برای دریافت مسیرهای مخازن
@app.route('/get-paths', methods=['GET'])
def get_paths():
    if not os.path.isfile(REPOS_FILE):
        return jsonify([])

    with open(REPOS_FILE, 'r') as f:
        paths = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    # بررسی ولید بودن مسیرها
    paths_with_status = [{"path": path, "isValid": validate_repo_path(path)} for path in paths]

    # مرتب‌سازی: ابتدا بر اساس ولید بودن، سپس بر اساس حروف الفبا
    sorted_paths = sorted(paths_with_status, key=lambda x: (not x["isValid"], x["path"].lower()))

    return jsonify(sorted_paths)
# API برای ذخیره مسیرهای مخازن
@app.route('/save-paths', methods=['POST'])
def save_paths():
    data = request.json
    paths = data.get('paths', [])
    with open(REPOS_FILE, 'w') as f:
        f.write("\n".join(paths))
    log("Paths updated successfully.")
    return jsonify({"message": "Paths saved successfully!"})

# API برای دریافت تنظیمات
@app.route('/get-settings', methods=['GET'])
def get_settings():
    settings = {
        "telegram_bot_token": TELEGRAM_BOT_TOKEN,
        "telegram_chat_id": TELEGRAM_CHAT_ID,
        "email_username": EMAIL_USERNAME
    }
    return jsonify(settings)

# API برای ذخیره تنظیمات
@app.route('/save-settings', methods=['POST'])
def save_settings():
    data = request.json
    with open(os.path.expanduser("~/auto_git_pusher/config/settings.py"), "w") as f:
        f.write(f"""
# Path to the repositories file
REPOS_FILE = "{REPOS_FILE}"

# Telegram bot settings
TELEGRAM_BOT_TOKEN = "{data.get('telegram_bot_token', '')}"
TELEGRAM_CHAT_ID = "{data.get('telegram_chat_id', '')}"

# Email settings
EMAIL_USERNAME = "{data.get('email_username', '')}"
""")
    log("Settings updated successfully.")
    return jsonify({"message": "Settings saved successfully!"})

# صفحه اصلی
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)