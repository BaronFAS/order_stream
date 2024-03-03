from telegram.ext import Updater

from flask_app.constants import CHAT_ID, TELEGRAM_TOKEN


def send_message(message):
    updater = Updater(token=TELEGRAM_TOKEN)
    updater.bot.send_message(chat_id=CHAT_ID, text=message)
    updater.stop()
