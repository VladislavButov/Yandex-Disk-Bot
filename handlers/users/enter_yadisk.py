import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from requests import post
from yadisk import YaDisk

from filters import IsPrivate
from handlers.users.menu import menu
from loader import dp

from data.config import CLIENT_ID, CLIENT_SECRET

from urllib.parse import urlencode

from states.connect_with_disk import ConnectWithYaDisk

from aiogram.utils.callback_data import CallbackData

from urllib.parse import urlparse, parse_qs


@dp.message_handler(IsPrivate(), state=ConnectWithYaDisk.connect)
async def process_code_message(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "🏠Главное меню":
        await menu(message)
        await state.finish()
        return

    data = await state.get_data()
    corr_dir = data.get("corr_dir")
    token = data.get("token")

    yadisk = YaDisk(token=token)
    files = yadisk.listdir(corr_dir)
    file_names = [f['name'] for f in files]
    if not file_names:
        await message.answer("Папка пуста")
    else:
        file_names_str = "\n".join(file_names)
        kb_list_of_files = InlineKeyboardMarkup()
        for file in file_names_str:
            button = InlineKeyboardButton(
                text=file,
                callback_data=f"select_file_{file}",
            )
            kb_list_of_files.add(button)
        await message.answer(f"Ваши файлы:\n{file_names_str}", reply_markup=kb_list_of_files)
        await ConnectWithYaDisk.get_files.set()
        await state.update_data(corr_dir=corr_dir)


@dp.callback_query_handler(state=ConnectWithYaDisk.connect)
async def process_code_message(query: types.CallbackQuery, state: FSMContext):
    answer = query.data

    if answer.startswith("select_file_"):
        data = await state.get_data()
        corr_dir = data.get("corr_dir")
        token = data.get("token")
        file_name = answer[12:]
        corr_dir = str(corr_dir) + str(file_name)

        yadisk = YaDisk(token=token)
        files = yadisk.listdir(corr_dir)
        file_names = [f['name'] for f in files]
        if not file_names:
            await query.answer("Папка пуста")
        else:
            file_names_str = "\n".join(file_names)
            kb_list_of_files = InlineKeyboardMarkup()
            for file in file_names_str:
                button = InlineKeyboardButton(
                    text=file,
                    callback_data=f"select_file_{file}",
                )
                kb_list_of_files.add(button)
            await query.message.answer(f"Ваши файлы:\n{file_names_str}", reply_markup=kb_list_of_files)
            await ConnectWithYaDisk.get_files.set()
            await state.update_data(corr_dir=corr_dir)
