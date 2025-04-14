from flask import Flask, request, jsonify, render_template
import os, json
from utils.logger import log
from utils.validator import validate_repo_path

app = Flask(__name__)

LOCAL_SHARE_DIR = os.path.expanduser("~/.local/share/auto_git_pusher/")
TOKEN_FILE = os.path.join(LOCAL_SHARE_DIR, "telegram_token.key")
SETTINGS_FILE = os.path.join(LOCAL_SHARE_DIR, "settings.json")
REPOS_FILE = os.path.join(LOCAL_SHARE_DIR, "repos.json")


# ------------------------- UTILS -------------------------

def read_settings_file():
    if not os.path.exists(SETTINGS_FILE):
        log(f"❌ File not found: {SETTINGS_FILE}")
        return {}
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        log(f"❌ Error decoding JSON in {SETTINGS_FILE}")
        return {}

def save_settings_file(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def read_repos_file():
    if not os.path.exists(REPOS_FILE):
        log(f"❌ File not found: {REPOS_FILE}")
        return []
    with open(REPOS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def write_repos_file(paths):
    with open(REPOS_FILE, "w") as f:
        f.write("# مسیرهای مخازن\n")
        for path in paths:
            f.write(f"{path}\n")


# ------------------------- API ROUTES -------------------------

@app.route('/')
def index():
    return render_template('index.html')

# Telegram settings (account + notifications)
@app.route('/telegram-settings', methods=['GET', 'POST'])
def telegram_settings():
    settings = read_settings_file()
    if request.method == 'GET':
        return jsonify({
            "telegram_chat_id": settings.get("TELEGRAM_CHAT_ID", ""),
            "notifications_enabled": settings.get("TELEGRAM_NOTIFICATIONS_ENABLED", False)
        })
    elif request.method == 'POST':
        data = request.json
        settings["TELEGRAM_CHAT_ID"] = data.get("telegram_chat_id", "")
        settings["TELEGRAM_NOTIFICATIONS_ENABLED"] = data.get("notifications_enabled", False)
        save_settings_file(settings)
        log(f"Telegram settings updated: Chat ID = {settings['TELEGRAM_CHAT_ID']}, Notifications = {settings['TELEGRAM_NOTIFICATIONS_ENABLED']}.")
        return jsonify({"message": "Telegram settings updated successfully!"})

# Email settings (account + notifications)
@app.route('/email-settings', methods=['GET', 'POST'])
def email_settings():
    settings = read_settings_file()
    if request.method == 'GET':
        return jsonify({
            "email_username": settings.get("EMAIL_USERNAME", ""),
            "notifications_enabled": settings.get("EMAIL_NOTIFICATIONS_ENABLED", False)
        })
    elif request.method == 'POST':
        data = request.json
        settings["EMAIL_USERNAME"] = data.get("email_username", "")
        settings["EMAIL_NOTIFICATIONS_ENABLED"] = data.get("notifications_enabled", False)
        save_settings_file(settings)
        log(f"Email settings updated: Username = {settings['EMAIL_USERNAME']}, Notifications = {settings['EMAIL_NOTIFICATIONS_ENABLED']}.")
        return jsonify({"message": "Email settings updated successfully!"})

@app.route('/get-theme', methods=['GET'])
def get_theme():
    settings = read_settings_file()
    return jsonify({"theme": settings.get("DEFAULT_THEME", "light")})

@app.route('/save-theme', methods=['POST'])
def save_theme():
    data = request.json
    theme = data.get('theme', 'light')
    settings = read_settings_file()
    settings["DEFAULT_THEME"] = theme
    save_settings_file(settings)
    log(f"Theme updated to {theme}.")
    return jsonify({"message": "Theme updated successfully!"})

@app.route('/validate-path', methods=['POST'])
def validate_path():
    path = request.json.get('path', '')
    return jsonify({"isValid": validate_repo_path(path)})

@app.route('/get-paths', methods=['GET'])
def get_paths():
    paths = read_repos_file()
    paths_with_status = [{"path": path, "isValid": validate_repo_path(path)} for path in paths]
    sorted_paths = sorted(paths_with_status, key=lambda x: (not x["isValid"], x["path"].lower()))
    return jsonify(sorted_paths)

@app.route('/save-paths', methods=['POST'])
def save_paths():
    paths = request.json.get('paths', [])
    write_repos_file(paths)
    log("Paths updated successfully.")
    return jsonify({"message": "Paths saved successfully!"})

# ------------------------- MAIN -------------------------
if __name__ == '__main__':
    app.run(debug=True)