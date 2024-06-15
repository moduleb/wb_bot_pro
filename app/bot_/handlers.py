from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app import text, db, parser
from app.bot_ import kb
from app.bot_.states import State_
from app.parser import ParserError

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)
    await state.set_state(State_.wait_for_url)


@router.message(State_.wait_for_url)
async def add(msg: Message, state: FSMContext):
    url = msg.text
    user_id = msg.from_user.id
    try:
        item_id = parser.get_item_id(url)
        data = parser.get_data(item_id)
        price = parser.get_price(data)
        title = parser.get_title(data)

        # Проверяем на дубликаты
        if db.get_items_by_user_id_and_item_id(user_id=user_id,
                                               item_id=item_id):
            await msg.answer(text.item_duplicate, reply_markup=kb.menu)
            return

        # Сохраняем в бд
        db.insert(user_id=user_id,
                  item_id=item_id,
                  price=price,
                  title=title)

        # Уведомляем об успехе
        mesg = await msg.answer(text.item_added, reply_markup=kb.menu)

    except ParserError as e:
        await msg.reply(str(e))


@router.callback_query(F.data == "items_list")
async def items_list(clbck: CallbackQuery, state: FSMContext):
    user_id = clbck.from_user.id
    if items := db.get_items_by_user_id(user_id):
        for item in items:
            await clbck.message.answer(
                text.item_info.format(title=item.title, price=item.price),
                reply_markup=kb.stop(item.item_id))

    else:
        await clbck.message.answer(text.no_items)
        await state.set_state(State_.wait_for_url)

    await clbck.message.delete()


@router.callback_query(lambda F: F.data.startswith("del"))
async def delete(clbck: CallbackQuery, state: FSMContext):
    db.delete(user_id=clbck.from_user.id,
              item_id=clbck.data.split('_')[1])
    await clbck.message.delete()
