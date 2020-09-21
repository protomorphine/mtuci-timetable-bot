from datetime import datetime
from datetime import timedelta
from flask import Flask, request
import json, telebot

bot = telebot.TeleBot(
    "1252210950:AAEoxZSkSaBMJkrFdflqnVme1MahMLekgXk", parse_mode="Markdown"
)
server = Flask(__name__)


def get_day_name(num):
    day_names = [
        "",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    return day_names[num]


def get_timetable(week_day):
    week = json.loads(open("json/week.json", "r", encoding="utf-8").read())
    parity_days = json.loads(
        open("json/parity_days.json", "r", encoding="utf-8").read()
    )
    week_days_ru = json.loads(
        open("json/week_days_ru.json", "r", encoding="utf-8").read()
    )
    is_week_even = False if (int(datetime.now().strftime("%V")) + 1) % 2 else True
    is_free_day = False

    week["thursday"] = parity_days["up"] if is_week_even else parity_days["down"]

    text = f"👨‍🏫 Расписание занятий на {week_days_ru[week_day]}\n"

    if week_day == "saturday" or week_day == "sunday":
        text += "\n*Пар нет!*"
        is_free_day = True
    else:
        day = week[week_day]
        for lesson in day:
            text += f"\n*Предмет:* {day[lesson]['name']}\n*Тип занятия:* {day[lesson]['type']}\n*Место проведения:* {day[lesson]['place']}\nНачало в *{day[lesson]['time']}*\n"

    return (text, is_free_day)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Привет, я помогу узнать тебе расписание",
        reply_markup=keyboard1,
    )


keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row("Сегодня", "Завтра", "Неделя")

keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row("Понедельник", "Вторник", "Среду")
keyboard2.row("Четверг", "Пятницу", "Назад")


@bot.message_handler(content_types=["text"])
def send_text(message):
    free_day = False
    week_days_ru = json.loads(
        open("json/week_days_ru.json", "r", encoding="utf-8").read()
    )
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
            message.chat.id, "Показать расписание на...", reply_markup=keyboard2,
        )
    elif message.text.lower() == "назад":
        bot.send_message(
            message.chat.id,
            "Привет, я помогу узнать тебе расписание",
            reply_markup=keyboard1,
        )
    else:
        res = ""
        for elem in week_days_ru:
            if week_days_ru[elem] == message.text:
                res = elem
                break
        day, free_day = get_timetable(res)
        bot.send_message(message.chat.id, day)

    if free_day:
        bot.send_sticker(
            message.chat.id,
            "CAACAgIAAxkBAANNX1N7fzzCXN0YEcxUdPAZ4s422HYAAmc2AALpVQUYGZMWsaF46GMbBA",
        )


@server.route("/bot", methods=["POST"])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://mtuci-raspisanie-bot.herokuapp.com/bot")
    return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get("PORT", 80))


# bot.polling()
