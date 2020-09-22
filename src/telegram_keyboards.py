import telebot


keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row("Сегодня", "Завтра", "Неделя")

# инлайн клавиатура с днями недели
inline_keyboard = telebot.types.InlineKeyboardMarkup()
monday_button = telebot.types.InlineKeyboardButton(
    text="Понедельник", callback_data="monday"
)
tuesday_button = telebot.types.InlineKeyboardButton(
    text="Вторник", callback_data="tuesday"
)
wednesday_button = telebot.types.InlineKeyboardButton(
    text="Среда", callback_data="wednesday"
)
thursday_button = telebot.types.InlineKeyboardButton(
    text="Четверг", callback_data="thursday"
)
friday_button = telebot.types.InlineKeyboardButton(
    text="Пятница", callback_data="friday"
)

inline_keyboard.add(monday_button, tuesday_button)
inline_keyboard.add(wednesday_button, thursday_button, friday_button)
