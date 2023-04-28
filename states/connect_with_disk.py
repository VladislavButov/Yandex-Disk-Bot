from aiogram.dispatcher.filters.state import StatesGroup, State


class ConnectWithYaDisk(StatesGroup):
    connect = State()
    get_files = State()
