from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
import threading

# Bu yerga tokenni to'g'ridan-to'g'ri yozamiz
TOKEN = "7747413362:AAHyv-MxISAf4YckcJuGuyx_hEXA7On8N0M"

# Bu yerga Railway'dagi APP_URL'ingni yoz (oxirida / bo'lmasin)
APP_URL = "https://web-production-af607.up.railway.app"

# Flask server yaratamiz
flask_app = Flask(__name__)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ok🗿")

# Har qanday xabarga javob
async def reply_ok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ok🗿")

# Flask route: webhookni sozlash
@flask_app.route("/setwebhook")
def set_webhook():
    app.bot.set_webhook(url=f"{APP_URL}/webhook")
    return "Webhook set!"

# Flask route: Telegram webhook uchun
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app.bot)
    app.update_queue.put(update)
    return "ok"

# Telegram botni backgroundda ishga tushirish
def run_bot():
    global app
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_ok))
    app.run_polling()

# Flask va Telegram birga ishlashi uchun
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    flask_app.run(host="0.0.0.0", port=8000)
