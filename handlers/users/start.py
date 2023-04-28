import sqlite3
from urllib.parse import urlencode

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import CLIENT_ID, CLIENT_SECRET
from filters import IsPrivate
from handlers.users.menu import menu
from keyboards.default import kb_menu
from loader import dp

from requests import post


@dp.message_handler(IsPrivate(), Command("start"), state="*")
async def command_start(message: types.Message, state: FSMContext = False):
    if state:
        await state.finish()
    args = message.get_args()
    baseurl = 'https://oauth.yandex.ru/'
    if args:
        code = args
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        data = urlencode(data)
        response = post(baseurl + "token", data).json()

        user_id = message.from_user.id
        access_token = response['access_token']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, access_token) VALUES (?, ?)", (user_id, access_token))
        conn.commit()
        cursor.close()
        conn.close()
        await message.answer("Ваш аккаунт успешно привязан.\n"
                             "Теперь вы можете полноценно пользоваться Яндекс Диском в Telegram!", reply_markup=kb_menu)

    else:
        await message.answer("Добро пожаловать в Яндекс Диск! Нажмите на кнопку "
                             "ЗАЙТИ В ДИСК чтобы привязать аккаунт",
                             reply_markup=kb_menu)

        await menu(message)
