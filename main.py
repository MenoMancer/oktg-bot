from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask, request
import os
import asyncio

TOKEN = "7747413362:AAHyv-MxISAf4YckcJuGuyx_hEXA7On8N0M"
APP_URL = "https://web-production-af607.up.railway.app"

app = Application.builder().token(TOKEN).build()
flask_app = Flask(__name__)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ok🗿")

# Har qanday xabarga javob
async def reply_ok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ok🗿")

# Flask route: webhookni sozlash
@flask_app.route("/setwebhook", methods=["GET"])
def set_webhook():
    asyncio.run(app.bot.set_webhook(f"{APP_URL}/webhook"))
    return "Webhook set!"

# Flask route: Telegram webhookdan xabar qabul qilish
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app.bot)
    asyncio.run(app.process_update(update))
    return "ok"

# Flask + bot handlerlar
if __name__ == "__main__":
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_ok))

    flask_app.run(host="0.0.0.0", port=8000)
