from aiogram.dispatcher.filters.state import StatesGroup, State


class ConnectWithYaDisk(StatesGroup):
    get_files = State()
    upload = State()
