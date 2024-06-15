from aiogram.fsm.state import StatesGroup, State


class State_(StatesGroup):
    wait_for_url = State()
    wait_for_stop = State()
