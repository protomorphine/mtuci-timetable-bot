from datetime import datetime, timedelta
from flask import Flask, request
import telebot, os

from src.parse_timetable import *
from src.telegram_keyboards import *


TOKEN = ""
LAZY_STICKER_ID = (
    "CAACAgIAAxkBAANNX1N7fzzCXN0YEcxUdPAZ4s422HYAAmc2AALpVQUYGZMWsaF46GMbBA"
)

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
webhook_server = Flask(__name__)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Привет, я помогу узнать тебе расписание",
        reply_markup=keyboard,
    )


@bot.message_handler(commands=["week"])
def start_message(message):
    bot.send_message(
        message.chat.id, "📅 Выбери день недели: ", reply_markup=inline_keyboard,
    )


@bot.message_handler(content_types=["text"])
def send_text(message):
    free_day = False
    if message.text.lower() == "сегодня":
        today, free_day = get_timetable(
            get_day_name(datetime.isoweekday(datetime.now()))
        )
        bot.send_message(message.chat.id, today)
    elif message.text.lower() == "завтра":
        tommorow, free_day = get_timetable(
            get_day_name(datetime.isoweekday(datetime.now() + timedelta(days=1)))
        )
        bot.send_message(message.chat.id, tommorow)
    elif message.text.lower() == "неделя":
        bot.send_message(
            message.chat.id, "📅 Выбери день недели: ", reply_markup=inline_keyboard,
        )
    if free_day:
        bot.send_sticker(
            message.chat.id, LAZY_STICKER_ID,
        )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        day, free_day = get_timetable(call.data)
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id, text=day,
        )


@webhook_server.route("/bot", methods=["POST"])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "!", 200


@webhook_server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://tg-timetable-bot.herokuapp.com/bot")
    return "?", 200


webhook_server.run(host="0.0.0.0", port=os.environ.get("PORT", 80))


# bot.remove_webhook()
# bot.polling()
