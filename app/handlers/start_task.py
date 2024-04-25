from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from app import kb

from app.states import StateClass
from app.utils.item import Item
from app.utils.sheduler import Scheduler

router= Router()

@router.callback_query(F.data == "get_url")
async def get_url(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer("Привет! Я помогу тебе отслеживать цену на товар, просто отправь мне ссылку на него.")
    await state.set_state(StateClass.wait_for_url)

@router.message(StateClass.wait_for_url)
async def start_task_confirm(msg: Message, state: FSMContext):
    url = msg.text
    user_id = msg.from_user.id
    try:
        item: Item = Item(url, user_id)
        await state.update_data(item=item)
        mesg = await msg.answer(str(item) + "\nВерно?", reply_markup=kb.iexit_kb)
        await state.set_state(StateClass.wait_for_start_confirm)
    except Exception as e:
        await msg.reply("Ошибка, попробуйте еще раз")

@router.callback_query(F.data == "start_task")
async def start_task(clbck: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item = data.get("item")
    await clbck.message.edit_text("Начали отслеживание")
    await clbck.message.answer("Начали отслеживание", reply_markup=ReplyKeyboardRemove())
    await Scheduler.start_task(func=Item.check_price, item=item, taskname=item.title)
    await state.clear()