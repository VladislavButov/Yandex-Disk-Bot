import sqlite3

from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from data.config import CLIENT_ID
from filters import IsPrivate
from handlers.users.menu import menu
from keyboards.default import kb_return
from loader import dp
from states.connect_with_disk import ConnectWithYaDisk
from states.upload_file import UploadFile

from yadisk import YaDisk


@dp.message_handler(IsPrivate(), text="Зайти в диск")
async def command_calculate(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('users.db')
    user_id = message.from_user.id
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()

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
        corr_dir = "/"
        files = yadisk.listdir(corr_dir)
        file_names = [f['name'] for f in files]
        if not file_names:
            await message.answer("Ваш Яндекс Диск пуст!")
            await menu(message)
        else:
            file_names_str = "\n".join(file_names)
            await message.answer(f"Ваши файлы:\n{file_names_str}", reply_markup=kb_return)
            await ConnectWithYaDisk.get_files.set()
            await state.update_data(token=data[1])
            await state.update_data(corr_dir=corr_dir)


@dp.message_handler(text="/upload")
async def upload_file(message: types.Message):
    await message.answer("Пришлите мне файл, который вы хотите загрузить!")
    await UploadFile.upload.set()


@dp.message_handler(content_types=['document'], state=UploadFile.upload)
async def save_file(message: types.Message, state: FSMContext):
    file_id = message.document.file_id
    file = await dp.bot.get_file(file_id)
    file_path = file.file_path
    file_name = file_path.split("/")[-1]
    with open(file_name, "wb") as f:
        await dp.bot.download_file_by_id(file_id, f)
    conn = sqlite3.connect('users.db')
    user_id = message.from_user.id
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    yadisk = YaDisk(token=data[1])
    yadisk.upload(file_name, file_name)
    await message.answer(f"Файл '{file_name}' загружен на Яндекс Диск!")
    await state.finish()


@dp.message_handler(IsPrivate(), text="👤Профиль")
async def command_calculate(message: types.Message):
    await message.answer("Профиль")
    # Добавить возможность привязать другой аккаунт или отвязать или рефку вообще ёбнуть


@dp.message_handler(IsPrivate(), text="🏠Главное меню")
async def work_with_orders(message: types.Message):
    await menu(message)
