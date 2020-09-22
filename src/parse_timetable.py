from datetime import datetime
import json


TEMPLATE = open("../output_template", "r", encoding="utf-8").read()
WEEK = open("../json/week.json", "r", encoding="utf-8").read()
PARRITY_DAYS = open("../json/parity_days.json", "r", encoding="utf-8").read()
WEEK_DAYS_RU = open("../json/week_days_ru.json", "r", encoding="utf-8").read()


def get_day_name(num):
    return [
        "",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ][num]


def get_timetable(week_day):
    week = json.loads(WEEK)
    parity_days = json.loads(PARRITY_DAYS)
    week_days_ru = json.loads(WEEK_DAYS_RU)
    is_week_even = False if ((int(datetime.now().strftime("%V")) + 1) % 2) else True
    is_free_day = False

    week["thursday"] = parity_days["down"] if is_week_even else parity_days["up"]

    text = f"👨‍🏫 Расписание занятий на {week_days_ru[week_day]}\n"

    if week_day == "saturday" or week_day == "sunday":
        text += "\n*Пар нет!*"
        is_free_day = True
    else:
        day = week[week_day]
        for class_ in day:
            text += eval(TEMPLATE)

    return (text, is_free_day)
