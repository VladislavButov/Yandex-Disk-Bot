import os
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

import requests
import io


@dp.message_handler(IsPrivate(), state=ConnectWithYaDisk.get_files)
async def process_code_message(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "🏠Главное меню":
        await menu(message)
        await state.finish()
        return
    elif answer == "🆙Загрузить файл":
        await message.answer("Пришлите мне файл, который вы хотите загрузить!")
        await ConnectWithYaDisk.upload.set()
        return
    if answer.startswith("select_file_"):
        data = await state.get_data()
        corr_dir = data.get("corr_dir")
        token = data.get("token")
        file_name = answer[12:]
        yadisk = YaDisk(token=token)
        path_to_file = f"{corr_dir}/{file_name}"
        meta = yadisk.get_meta(path_to_file)
        if meta["type"] == "file":
            download_link = yadisk.get_download_link(path_to_file)
            response = requests.get(download_link)
            file_bytes = io.BytesIO(response.content)
            file_bytes.name = file_name
            await dp.bot.send_document(message.from_user.id, document=file_bytes)
        else:
            corr_dir = path_to_file
            files = yadisk.listdir(corr_dir)
            file_names = [f['name'] for f in files]
            if not file_names:
                await message.answer("Папка пуста")
                await ConnectWithYaDisk.get_files.set()
                await state.update_data(corr_dir=corr_dir)
                return
        files = yadisk.listdir(corr_dir)
        file_names = [f['name'] for f in files]
        file_names_str = "\n".join(file_names)
        kb_list_of_files = InlineKeyboardMarkup()
        for file in file_names_str.split("\n"):
            button = InlineKeyboardButton(
                text=file,
                callback_data=f"select_file_{file}",
            )
            kb_list_of_files.add(button)
        await message.answer(f"Ваши файлы:\n{file_names_str}", reply_markup=kb_list_of_files)
        await ConnectWithYaDisk.get_files.set()
        await state.update_data(corr_dir=corr_dir)


@dp.callback_query_handler(state=ConnectWithYaDisk.get_files)
async def process_code_message(query: types.CallbackQuery, state: FSMContext):
    answer = query.data

    if answer.startswith("select_file_"):
        data = await state.get_data()
        corr_dir = data.get("corr_dir")
        token = data.get("token")
        file_name = answer[12:]
        yadisk = YaDisk(token=token)
        path_to_file = f"{corr_dir}/{file_name}"
        meta = yadisk.get_meta(path_to_file)
        if meta["type"] == "file":
            download_link = yadisk.get_download_link(path_to_file)
            response = requests.get(download_link)
            file_bytes = io.BytesIO(response.content)
            file_bytes.name = file_name
            await dp.bot.send_document(query.from_user.id, document=file_bytes)
        else:
            corr_dir = path_to_file
            files = yadisk.listdir(corr_dir)
            file_names = [f['name'] for f in files]
            if not file_names:
                await query.answer("Папка пуста")
                await ConnectWithYaDisk.get_files.set()
                await state.update_data(corr_dir=corr_dir)
                return
        files = yadisk.listdir(corr_dir)
        file_names = [f['name'] for f in files]
        file_names_str = "\n".join(file_names)
        kb_list_of_files = InlineKeyboardMarkup()
        for file in file_names_str.split("\n"):
            button = InlineKeyboardButton(
                text=file,
                callback_data=f"select_file_{file}",
            )
            kb_list_of_files.add(button)
        await query.message.answer(f"Ваши файлы:\n{file_names_str}", reply_markup=kb_list_of_files)
        await ConnectWithYaDisk.get_files.set()
        await state.update_data(corr_dir=corr_dir)


@dp.message_handler(content_types=['document'], state=ConnectWithYaDisk.upload)
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
    datta = await state.get_data()
    corr_dir = datta.get("corr_dir")
    yadisk = YaDisk(token=data[1])
    yadisk.upload(file_name, corr_dir + "/" +file_name)
    await message.answer(f"Файл '{file_name}' загружен на Яндекс Диск!")
    os.remove(f"documents/{file_name}")
    await ConnectWithYaDisk.get_files.set()

