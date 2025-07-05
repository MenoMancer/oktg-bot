from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.environ.get("BOT_TOKEN")
APP_URL = os.environ.get("APP_URL")

app = Flask(__name__)
telegram_app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ok🗿")

async def reply_ok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ok🗿")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, reply_ok))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "ok", 200

@app.route("/", methods=["GET"])
def set_webhook():
    telegram_app.bot.set_webhook(url=f"{APP_URL}/{TOKEN}")
    return "Webhook set!", 200

if __name__ == "__main__":
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=f"{APP_URL}/{TOKEN}",
    )
