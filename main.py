import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from yadisk import YaDisk
from aiogram.utils import executor
from keyboards.default.keyboard_menu import ikb

logging.basicConfig(level=logging.INFO)

bot = Bot(token='6117875309:AAHOok95JNdKBjzmQRBkMpLRUGK4Z3OcNqc')
dp = Dispatcher(bot)

yadisk = YaDisk(token='y0_AgAAAAAxHul9AAnMtwAAAADh3k3ptoPpRDo5T2SZUr2l2xoBNTJ97EA')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Добро пожаловать в Яндекс Диск", reply_markup=ikb)


@dp.message_handler(commands=['list'])
async def list_files(message: types.Message):
    files = yadisk.listdir('/')
    file_names = [f['name'] for f in files]
    if not file_names:
        await message.answer("Ваш Яндекс Диск пуст!")
    else:
        file_names_str = "\n".join(file_names)
        await message.answer(f"Ваши файлы:\n{file_names_str}")


@dp.message_handler(commands=['upload'])
async def upload_file(message: types.Message):
    await message.answer("Пришлите мне файл, который вы хотите загрузить!")
    await bot.register_next_step_handler(message, save_file)


async def save_file(message: types.Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = file_path.split("/")[-1]
    with open(file_name, "wb") as f:
        await bot.download_file_by_id(file_id, f)
    yadisk.upload(file_name, file_name)
    await message.answer(f"Файл '{file_name}' загружен на Яндекс Диск!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
