from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup


HELP = 'Помощь'
PARCER = 'Парсер'


def option_buttons():
    keyboard = [
        [
            KeyboardButton(HELP),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


def option_buttons_pars():
    keyboard = [
        [
            KeyboardButton(PARCER),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
