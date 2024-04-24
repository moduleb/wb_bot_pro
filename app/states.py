from aiogram.fsm.state import StatesGroup, State


class StateClass(StatesGroup):
    wait_for_url = State()
