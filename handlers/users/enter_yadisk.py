import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from requests import post
from yadisk import YaDisk

from filters import IsPrivate
from loader import dp

from data.config import CLIENT_ID, CLIENT_SECRET

from urllib.parse import urlencode

from states.connect_with_disk import ConnectWithYaDisk

from aiogram.utils.callback_data import CallbackData

from urllib.parse import urlparse, parse_qs



@dp.message_handler(IsPrivate(), state=ConnectWithYaDisk.connect)
async def process_code_message(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('users.db')
    user_id = message.from_user.id
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()

    if data is None:
        baseurl = 'https://oauth.yandex.ru/'
        url_button = types.InlineKeyboardButton(text="Запросить доступ",
                                                url=baseurl + "authorize?response_type=code&client_id={}".format(CLIENT_ID),
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
    await ConnectWithYaDisk.get_files.set()




