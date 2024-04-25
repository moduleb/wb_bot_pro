from aiogram.fsm.state import StatesGroup, State


class StateClass(StatesGroup):
    wait_for_url = State()
    wait_for_start_confirm = State()
    wait_for_choose_task_to_stop = State()
    wait_for_stop_confirm = State()