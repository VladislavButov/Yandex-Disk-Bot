from aiogram.dispatcher.filters.state import StatesGroup, State


class UploadFile(StatesGroup):
    upload = State()
