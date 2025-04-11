from telegram import Update # type: ignore
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes # type: ignore
import os
import subprocess
import re


BOT_TOKEN = "8067735833:AAEISZS2wtx_ON6miGfs6axJlwWRFABzn-E"
user_path = os.path.expanduser("~")


def scanner(repos_file):
    if not os.path.isfile(repos_file):
        message =(f"❌ File not found: {repos_file}")
        return message

    with open(repos_file, "r") as f:
        repos = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    if not repos:
        message =("⚠️ Warning: The repos.txt file is empty (only comments or blank lines). Please add your git repositories.")
        # Optionally reset the file with sample content
        with open(repos_file, "w") as f:
            f.write("# Add your git repositories here\n")
            f.write("# Example: /path/to/your/repo\n")
        return message
    
    message = ""
    for path in repos:
        Home_path = path.replace(user_path, "", 1)
        result = subprocess.run(["git", "-C", path, "remote", "get-url", "main"],
                                capture_output=True, text=True)
        if result.returncode == 0:
            url = result.stdout.strip()
            message += f"<a href=\"{path}\"><b>{Home_path}</b></a> ➜ <a href=\"{url}\">link</a>\n"
        else:
            message += f"<a href=\"{path}\"><b>{Home_path}</b></a> ➜ <i>remote not found</i>\n"

    return message

#   /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("welcome to \"Auto Git Pusher\" bot\n")

#   /path
async def path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(scanner(os.path.expanduser("~/auto_git_pusher/config/repos.txt")), parse_mode='HTML')
    
    
#   /add_repo
async def add_repo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Extract the repository path from the user's message
        input_text = update.message.text
        input_path = input_text.split(maxsplit=1)[1]  # Get the second part of the message (after the command)

        # Expand the user's home directory if needed
        input_path = os.path.expanduser(input_path)

        # Path to the repos.txt file
        repos_file = os.path.expanduser("~/auto_git_pusher/config/repos.txt")

        # Check if the path is valid and add it to repos.txt
        with open(repos_file, "a") as f:
            f.write('\n' + input_path)
        await update.message.reply_text(f"✅ Repository path added successfully: {input_path}")
        
    except IndexError:
        # Handle the case where the user didn't provide a path
        await update.message.reply_text("❌ Please provide a repository path. Example: /add_repo /path/to/repo")

#   /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("this bot will help you to push your changes to the git repository\n"
                                    "please use /path command to see your repositories\n"
                                    "and if you want to add a new repository please add it in repos.txt file\n"
                                    "and then use /add_repo command to see your new repositories")
    
#   /log
async def log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_file = ("~/.local/share/Auto_Git_Pusher/logs/run.log")
    
    # check foe exist
    if not os.path.isfile(log_file):
        await update.message.reply_text("❌ Log file not found.")
        return

    # read file
    with open(log_file, "r") as f:
        log_content = f.read()

    # send
    await update.message.reply_text(log_content.strip())



# setting bot application
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("path", path))
    app.add_handler(CommandHandler("add_repo", add_repo))  # Add this line
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("log", log))

    # run bot
    app.run_polling()
    
    
if __name__ == '__main__':
    main()
