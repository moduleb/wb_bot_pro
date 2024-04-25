from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from app.utils.sheduler import Scheduler

menu = [
    [InlineKeyboardButton(text="Добавить товар для отслеживания", callback_data="get_url")],
     [InlineKeyboardButton(text="Остановить отслеживание товара", callback_data="choose_task_to_stop")]]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="start_task"),
     InlineKeyboardButton(text="◀️ Назад", callback_data="menu"),
     ]])

def all_tasks(kb_info):
    all_tasks_kb = []
    for task_id, taskname in kb_info.items():
        all_tasks_kb.append([InlineKeyboardButton(text=taskname, callback_data=f"confirm_stop_task_{task_id}")])
    return InlineKeyboardMarkup(inline_keyboard=all_tasks_kb)

def iexit_kb_stop(task_id):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data=f"stop_task_{task_id}"),
     InlineKeyboardButton(text="◀️ Назад", callback_data="menu"),
     ]])

