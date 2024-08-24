from typing import Union

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import websockets
import text
import kb
import config
from ws import ws_manager

from shared import parser
from shared.db import service
from states import State_
from shared.parser import ParserError

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
    await ws_manager.send(f"hello from bot {msg}")
    sent_msgs.append(sent_msg)

    # Записываем сообщения для последующего удаления
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

    if items := await service.get_items_by_user_id(user_id):
        for item in items:
            sent_msg = await bot.send_message(
                chat_id=user_id,
                text=text.item_info.format(title=item.title, price=item.price, url=item.url),
                reply_markup=kb.stop(item.item_id),
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
    # Удаляем предыдущие сообщения
    data = await state.get_data()
    await delete_msgs(msg.bot, data.get('msgs'))

    url = msg.text
    user_id = msg.from_user.id
    sent_msgs = []

    try:
        item_id = parser.get_item_id(url)
        data = parser.get_data(item_id)
        price = parser.get_price(data)
        title = parser.get_title(data)

        # Проверяем на дубликаты
        if await service.get_item_by_user_id_and_item_id(user_id=user_id, item_id=item_id):
            sent_msg = await msg.answer(text=text.item_duplicate, reply_markup=kb.menu)
            sent_msgs.append(sent_msg)
            return

        # Сохраняем в бд
        await service.insert(user_id=user_id,
                             item_id=item_id,
                             price=price,
                             title=title,
                             url=url)

        # Уведомляем об успехе
        sent_msg = await msg.answer(text=text.item_added, reply_markup=kb.menu)
        sent_msgs.append(sent_msg)

    except ParserError as e:
        sent_msg = await msg.reply(str(e),
                                   disable_web_page_preview=True)
        sent_msgs.append(sent_msg)

    # Записываем сообщения для последующего удаления
    data['msgs'] = sent_msgs
    await state.set_data(data)


@router.callback_query(F.data.startswith("del"))
async def delete(callback: CallbackQuery):
    await service.delete(user_id=callback.from_user.id,
                         item_id=callback.data.split('_')[1])
    await callback.message.delete()
