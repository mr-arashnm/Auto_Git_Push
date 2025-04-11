from telegram.ext import CommandHandler

def start(update, context):
    update.message.reply_text("سلام! آماده‌ام مسیرها رو برات ذخیره کنم.")

def addpath(update, context):
    path = ' '.join(context.args)
    if path:
        with open('paths.txt', 'a') as f:
            f.write(path + '\n')
        update.message.reply_text(f'✅ مسیر اضافه شد:\n{path}')
    else:
        update.message.reply_text('❗ لطفاً مسیر رو بنویس: /addpath your_path')

# ...
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("addpath", addpath))
