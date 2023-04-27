import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InputFile
import yadisk
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import CallbackQuery


logging.basicConfig(level=logging.INFO)

bot = Bot(token='')
dp = Dispatcher(bot)

y = yadisk.YaDisk(token="")
print(y.check_token())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Загрузить файл", callback_data="upload"))
    await message.answer("Добро пожаловать в Яндекс Диск", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'upload')
async def process_upload(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Пришлите мне файл, который вы хотите загрузить!")
    # Remove the "Upload" button from the keyboard
    await bot.send_message(callback_query.from_user.id, "Вы можете вернуться к списку файлов командой /list",
                           reply_markup=ReplyKeyboardRemove())
    # Register the handler for the next message the user sends, which will be the file
    dp.register_message_handler(save_file)


@dp.message_handler(content_types=['document'])
async def save_file(message: types.Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = file_path.split("/")[-1]
    with open(file_name, "wb") as f:
        await bot.download_file_by_id(file_id, f)
    y.upload(file_name, file_name)
    await message.answer(f"Файл '{file_name}' загружен на Яндекс Диск!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
