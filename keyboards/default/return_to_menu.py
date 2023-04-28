from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_return = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🆙Загрузить файл")
        ],
        [
            KeyboardButton(text="🏠Главное меню"),
        ]
    ],
    resize_keyboard=True
)
