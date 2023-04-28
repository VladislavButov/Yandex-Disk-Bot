from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsPrivate
from handlers.users.menu import menu
from loader import dp


@dp.message_handler(IsPrivate(), text="/help", state="*")
async def command_help(message: types.Message, state: FSMContext = False):
    if state:
        await state.finish()
    await message.answer("Если возникли сложности при использовании бота, напишите нашим администраторам:"
                         " @vladislavmain"
                         " @swyatoslavik")
    await menu(message)