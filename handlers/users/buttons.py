import sqlite3

from aiogram import types

from data.config import CLIENT_ID
from filters import IsPrivate
from handlers.users.menu import menu
from loader import dp
from states.connect_with_disk import ConnectWithYaDisk

from yadisk import YaDisk


@dp.message_handler(IsPrivate(), text="Зайти в диск")
async def command_calculate(message: types.Message):
    conn = sqlite3.connect('users.db')
    user_id = message.from_user.id
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    print(data)
    if data is None:
        baseurl = 'https://oauth.yandex.ru/'
        url_button = types.InlineKeyboardButton(text="Запросить доступ",
                                                url=baseurl + "authorize?response_type=code&client_id={}".format(
                                                    CLIENT_ID),
                                                )

        keyboard = types.InlineKeyboardMarkup().add(url_button)
        await message.answer("Разрешить доступ к аккаунту", reply_markup=keyboard)
    else:
        yadisk = YaDisk(token=data[1])
        files = yadisk.listdir('/')
        file_names = [f['name'] for f in files]
        if not file_names:
            await message.answer("Ваш Яндекс Диск пуст!")
        else:
            file_names_str = "\n".join(file_names)
            await message.answer(f"Ваши файлы:\n{file_names_str}")


@dp.message_handler(IsPrivate(), text="👤Профиль")
async def command_calculate(message: types.Message):
    await message.answer("Профиль")
    # Добавить возможность привязать другой аккаунт или отвязать или рефку вообще ёбнуть


@dp.message_handler(IsPrivate(), text="🏠Главное меню")
async def work_with_orders(message: types.Message):
    await menu(message)



