from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

menu = [
    [InlineKeyboardButton(text="Добавить товар для отслеживания", callback_data="get_url"),
     InlineKeyboardButton(text="Остановить отслеживание товара", callback_data="stop_task")]]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="start_task"),
     InlineKeyboardButton(text="◀️ Назад", callback_data="menu"),
     ]])
