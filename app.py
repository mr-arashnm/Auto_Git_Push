from flask import Flask, request, jsonify, render_template # type: ignore
import os, json
from utils.logger import log
from utils.validator import validate_repo_path

app = Flask(__name__)

LOCAL_SHARE_DIR = os.path.expanduser("~/.local/share/auto_git_pusher/")
TOKEN_FILE = os.path.join(LOCAL_SHARE_DIR, "telegram_token.key")
SETTINGS_FILE = os.path.join(LOCAL_SHARE_DIR, "settings.json")
#REPOS_FILE = os.path.join(LOCAL_SHARE_DIR, "repos.json")


# ------------------------- UTILS -------------------------

def read_file(path):
    if not os.path.exists(path):
        log(f"❌ File not found: {path}")
        return {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        log(f"❌ Error decoding JSON in {path}")
        return {}
    
def save_settings_file(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def write_repos_file(paths):
    with open(SETTINGS_FILE, "w") as f:
        f.write("# مسیرهای مخازن\n")
        for path in paths:
            f.write(f"{path}\n")


# ------------------------- API ROUTES -------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-paths', methods=['GET'])
def get_paths():
    repos = read_file(SETTINGS_FILE)
    if request.method == 'GET':
        return jsonify({
            "repos": repos.get("REPOS_FILE", [])
        })
        
@app.route('/save-paths', methods=['POST'])
def save_paths():
    paths = request.json.get('paths', [])
    write_repos_file(paths)
    log("Paths updated successfully.")
    return jsonify({"message": "Paths saved successfully!"})

# Telegram settings (account + notifications)
@app.route('/telegram-settings', methods=['GET', 'POST'])
def telegram_settings():
    settings = read_file(SETTINGS_FILE)
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
    settings = read_file(SETTINGS_FILE)
    if request.method == 'GET':
        return jsonify({
            "email_username": settings.get("EMAIL_USERNAME", ""),
            "notifications_enabled": settings.get("EMAIL_NOTIFICATIONS_ENABLED", False)
        })
    elif request.method == 'POST':
        data = request.json
        settings["EMAIL_USERNAME"] = data.get("email_username", "")
        settings["EMAIL_NOTIFICATIONS_ENABLED"] = data.get("notifications_enabled", "")
        save_settings_file(settings)
        log(f"Email settings updated: Username = {settings['EMAIL_USERNAME']}, Notifications = {settings['EMAIL_NOTIFICATIONS_ENABLED']}.")
        return jsonify({"message": "Email settings updated successfully!"})

@app.route('/get-theme', methods=['GET'])
def get_theme():
    settings = read_file(SETTINGS_FILE)
    return jsonify({"theme": settings.get("DEFAULT_THEME", "light")})

@app.route('/save-theme', methods=['POST'])
def save_theme():
    data = request.json
    theme = data.get('theme', 'light')
    settings = read_file(SETTINGS_FILE)
    settings["DEFAULT_THEME"] = theme
    save_settings_file(settings)
    log(f"Theme updated to {theme}.")
    return jsonify({"message": "Theme updated successfully!"})

@app.route('/validate-path', methods=['POST'])
def validate_path():
    path = request.json.get('path', '')
    return jsonify({"isValid": validate_repo_path(path)})


# ------------------------- MAIN -------------------------
if __name__ == '__main__':
    app.run(debug=True)