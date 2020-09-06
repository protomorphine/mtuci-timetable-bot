from datetime import datetime
from datetime import timedelta
import json, telebot

bot = telebot.TeleBot(
    "1252210950:AAEoxZSkSaBMJkrFdflqnVme1MahMLekgXk", parse_mode="Markdown"
)


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
    week = json.loads(open("json\week.json", "r", encoding="utf-8").read())
    parity_days = json.loads(
        open("json\parity_days.json", "r", encoding="utf-8").read()
    )
    week_days_ru = json.loads(
        open("json\week_days_ru.json", "r", encoding="utf-8").read()
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
keyboard1.row("Сегодня", "Завтра")


@bot.message_handler(content_types=["text"])
def send_text(message):
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
    if free_day:
        bot.send_sticker(
            message.chat.id,
            "CAACAgIAAxkBAANNX1N7fzzCXN0YEcxUdPAZ4s422HYAAmc2AALpVQUYGZMWsaF46GMbBA",
        )


@bot.message_handler(content_types=["sticker"])
def sticker_id(message):
    print(message)


bot.polling()
