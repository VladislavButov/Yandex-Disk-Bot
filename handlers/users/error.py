from aiogram import types

from filters import IsPrivate
from handlers.users.menu import menu
from loader import dp


@dp.message_handler(IsPrivate())
async def command_error(message: types.Message):
    await message.answer("🌧 Неизвестная команда")
    args = message.get_args()
    print(args)
    await menu(message)
