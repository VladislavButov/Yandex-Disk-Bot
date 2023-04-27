from aiogram import types

from filters import IsPrivate
from handlers.users.menu import menu
from loader import dp
from states.connect_with_disk import ConnectWithYaDisk

from yadisk import YaDisk


@dp.message_handler(IsPrivate(), text="Зайти в диск")
async def command_calculate(message: types.Message):
    # yadisk = YaDisk(token='8d93b64cec2f460fa7e2a77d765696de')
    # files = yadisk.listdir('/')
    # file_names = [f['name'] for f in files]
    # if not file_names:
    #     await message.answer("Ваш Яндекс Диск пуст!")
    # else:
    #     file_names_str = "\n".join(file_names)
    #     await message.answer(f"Ваши файлы:\n{file_names_str}")
    await message.answer("Подключаем к диску")
    await ConnectWithYaDisk.connect.set()


@dp.message_handler(IsPrivate(), text="👤Профиль")
async def command_calculate(message: types.Message):
    await message.answer("Профиль")
    # Добавить возможность привязать другой аккаунт или отвязать или рефку вообще ёбнуть


@dp.message_handler(IsPrivate(), text="🏠Главное меню")
async def work_with_orders(message: types.Message):
    await menu(message)



