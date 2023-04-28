from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Зайти в диск"),
        ],
        [
            KeyboardButton(text="👤Профиль"),
            KeyboardButton(text="👨‍💻Помощь"),
        ],
        [
            KeyboardButton(text="❓Справочный центр")
        ]
    ],
    resize_keyboard=True
)
