import os
import subprocess
import json


# مسیرهای مورد نیاز
LOCAL_SHARE_DIR = os.path.expanduser("~/.local/share/auto_git_pusher/")
TOKEN_FILE = os.path.join(LOCAL_SHARE_DIR, "telegram_token.key")
SETTINGS_FILE = os.path.join(LOCAL_SHARE_DIR, "settings.json")
REPOS_FILE = os.path.join(LOCAL_SHARE_DIR, "repos.json")

# تنظیمات پیش‌فرض
DEFAULT_SETTINGS = {
    "REPOS_FILE": "~/.local/share/auto_git_pusher/repos.json",
    "TELEGRAM_CHAT_ID": "mr_arashnm",
    "TELEGRAM_NOTIFICATIONS_ENABLED": True,
    "EMAIL_USERNAME": "your_email@example.com",
    "EMAIL_NOTIFICATIONS_ENABLED": True,
    "DEFAULT_THEME": "dark"
}

def install_dependencies():
    """
    نصب وابستگی‌های مورد نیاز پروژه.
    """
    print("Installing dependencies...")
    if not os.path.exists("requirements.txt"):
        print("Error: requirements.txt not found. Please create the file and list your dependencies.")
        return
    try:
        subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")

def setup_directories():
    """
    ایجاد پوشه‌های مورد نیاز.
    """
    print(f"Creating directory: {LOCAL_SHARE_DIR}")
    os.makedirs(LOCAL_SHARE_DIR, exist_ok=True)
    print("Directories created successfully.")

def setup_telegram_token():
    """
    دریافت و ذخیره توکن تلگرام.
    """
    if not os.path.exists(TOKEN_FILE):
        token = input("Enter your Telegram bot token: ").strip()
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        os.chmod(TOKEN_FILE, 0o600)  # محدود کردن دسترسی به فایل
        print("Telegram bot token saved successfully.")
    else:
        print("Telegram bot token already exists. Skipping...")

def setup_settings():
    """
    ایجاد فایل تنظیمات اولیه.
    """
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
        print("Default settings saved successfully.")
    else:
        print("Settings file already exists. Skipping...")
        
def setup_repos_file():
    """
    ایجاد فایل repos.json در مسیر ~/.local/share/auto_git_pusher/
    """
    # اطمینان از وجود پوشه
    os.makedirs(os.path.dirname(REPOS_FILE), exist_ok=True)
    
    # ایجاد فایل repos.json در صورت عدم وجود
    if not os.path.exists(REPOS_FILE):
        with open(REPOS_FILE, "w") as f:
            json.dump([], f, indent=4)  # فایل JSON خالی
        print(f"Default repos file created at {REPOS_FILE}")
    else:
        print(f"Repos file already exists at {REPOS_FILE}")

def main():
    """
    اجرای فرآیند نصب.
    """
    print("Starting installation...")
    install_dependencies()
    setup_directories()
    setup_telegram_token()
    setup_settings()
    setup_repos_file()
    print("Installation completed successfully!")

if __name__ == "__main__":
    main()