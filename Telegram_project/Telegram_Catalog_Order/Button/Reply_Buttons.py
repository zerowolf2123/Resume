from telegram import ReplyKeyboardMarkup, KeyboardButton

CATALOG = 'Каталог'
BOT = 'Сведения'


def option_buttons():
    keyboard = [
        [
            KeyboardButton(CATALOG),
            KeyboardButton(BOT)
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )