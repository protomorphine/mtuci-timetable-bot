import json, telebot


week_days_ru = json.loads(open("json/week_days_ru.json", "r", encoding="utf-8").read())
print(week_days_ru)

print(week_days_ru.keys())

for keys in week_days_ru:
    print(keys)
    print(week_days_ru[keys])
