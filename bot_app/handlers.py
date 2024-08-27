import json
from typing import Union


from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import kb
import text
from parser_func import parser

from shared.db import service

from states import State_
from ws import ws_manager

router = Router()



async def delete_msgs(bot: Bot, msgs: list[Message]) -> None:
    if msgs:
        for msg in msgs:
            try:
                await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
            except TelegramBadRequest:  # если сообщения с таким id не существует...
                pass


@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    # Удаляем предыдущие сообщения
    data = await state.get_data()
    await delete_msgs(msg.bot, data.get('msgs'))

    sent_msgs = []
    sent_msg = await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)

    # Записываем сообщения для последующего удаления
    sent_msgs.append(sent_msg)
    data['msgs'] = sent_msgs
    await state.set_data(data)

    await state.set_state(State_.wait_for_url)


@router.message(Command("tasks"))
@router.callback_query(F.data == "items_list")
async def items_list(event: Union[CallbackQuery, Message], state: FSMContext):
    # Удаляем предыдущие сообщения
    data = await state.get_data()
    await delete_msgs(event.bot, data.get('msgs'))

    user_id = event.from_user.id
    bot = event.bot
    sent_msgs = []

    # Формируем сообщение для отправки по websocket
    message = {
        "action": "get_all",
        "user_id": user_id
    }

    # Отправляем сообщение по websocket
    response_row = await ws_manager.send(message)
    response_dict = json.loads(response_row)
    items = response_dict.get("data")

    if items:
        for item in items:
            sent_msg = await bot.send_message(
                chat_id=user_id,
                text=text.item_info.format(title=item.get("title"), price=item.get("price"), url=item.get("url")),
                reply_markup=kb.stop(item.get("item_id")),
                parse_mode="Markdown",
                disable_web_page_preview=True)
            sent_msgs.append(sent_msg)

    else:
        sent_msg = await bot.send_message(
            chat_id=user_id,
            text=text.no_items)
        sent_msgs.append(sent_msg)

        await state.set_state(State_.wait_for_url)

    # Записываем сообщения для последующего удаления
    data['msgs'] = sent_msgs
    await state.set_data(data)


@router.message(State_.wait_for_url)
async def add(msg: Message, state: FSMContext):
    url = msg.text
    bot = msg.bot
    user_id = msg.from_user.id
    sent_msgs = []

    # Удаляем предыдущие сообщения
    data = await state.get_data()
    await delete_msgs(bot, data.get('msgs'))

    try:
        data = await parser(url)
        price = data.get("price")
        title = data.get("title")
        item_id = data.get("item_id")

        # Формируем сообщение для отправки по websocket
        message = {
            "action": "create",
            "user_id": user_id,
            "price":price,
            "title":title,
            "url": url,
            "item_id": item_id
        }

        # Отправляем сообщение по websocket
        response_row = await ws_manager.send(message)
        try:
            response_dict = json.loads(response_row)
        except Exception as e:
            print(str(e))
            response_dict = {}

        # Уведомляем об успехе
        if response_dict.get("success"):
            msg_to_send = text.item_added
        else:
            msg_to_send = text.error

        sent_msg = await msg.answer(text=msg_to_send, reply_markup=kb.menu)
        sent_msgs.append(sent_msg)


    except KeyError as e:
        sent_msg = await msg.reply(str(e),
                                   disable_web_page_preview=True)
        sent_msgs.append(sent_msg)

    # Записываем сообщения для последующего удаления
    data['msgs'] = sent_msgs
    await state.set_data(data)


@router.callback_query(F.data.startswith("del"))
async def delete(callback: CallbackQuery):

    user_id = callback.from_user.id
    item_id = callback.data.split('_')[1]

    # Формируем сообщение для отправки по websocket
    message = {
        "action": "delete",
        "user_id": user_id,
        "item_id": item_id,
    }

    # Отправляем сообщение по websocket
    response = await ws_manager.send(message)

    await service.delete(user_id=callback.from_user.id,
                         item_id=callback.data.split('_')[1])
    await callback.message.delete()
