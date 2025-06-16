from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def location():
    button = [[KeyboardButton(text="📍 Отправить геолокацию", request_location=True)],
              [KeyboardButton(text="✍️ Ввести вручную")]
             ]

    return ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
