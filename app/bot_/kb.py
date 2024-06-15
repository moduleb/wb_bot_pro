from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

menu = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Мои отслеживания...", callback_data="items_list")
]])


def stop(item_id):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Удалить", callback_data=f'del_{item_id}')
    ]])


# exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
