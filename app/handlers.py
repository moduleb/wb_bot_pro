from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from app import kb, text
from app.utils.item import Item
from app.states import StateClass
from app.utils.sheduler import Scheduler

router = Router()


# await state.clear()
@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.callback_query(F.data == "get_url")
async def get_url(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer("Привет! Я помогу тебе отслеживать цену на товар, просто отправь мне ссылку на него.")
    await state.set_state(StateClass.wait_for_url)


@router.callback_query(F.data == "stop_task")
async def stop_task(clbck: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item = data["item"]
    await Scheduler.stop_task(item._id)
    await clbck.message.answer("ok")


@router.message(StateClass.wait_for_url)
async def confirmation(msg: Message, state: FSMContext):
    url = msg.text
    user_id = msg.from_user.id
    try:
        item: Item = Item(url, user_id)
        await state.update_data(item=item)
        mesg = await msg.answer(str(item) + "\nВерно?", reply_markup=kb.iexit_kb)
    except Exception as e:
        await msg.reply("Ошибка")


@router.callback_query(F.data == "start_task")
async def start_task(clbck: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item = data.get("item")
    await clbck.message.edit_text("Начали отслеживание")
    await clbck.message.answer("Начали отслеживание", reply_markup=ReplyKeyboardRemove())
    await Scheduler.start_task(item)

# @router.message(Command("start"))
# async def start_handler(msg: Message):
#     await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")
#
# @router.message()
# async def message_handler(msg: Message):
#     await msg.answer(f"Твой ID: {msg.from_user.id}")

# @router.message(Command("start"))
# async def start_handler(msg: Message):
#     await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)
#
# @router.callback_query(F.data == "generate_text")
# async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
#     await state.set_state(Gen.text_prompt)
#     await clbck.message.edit_text(text.gen_text)
#     await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)
#
# @router.message(Gen.text_prompt)
# @flags.chat_action("typing")
# async def generate_text(msg: Message, state: FSMContext):
#     prompt = msg.text
#     mesg = await msg.answer(text.gen_wait)
#     res = prompt
#     if not res:
#         return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
#     await mesg.edit_text(res + text.text_watermark, disable_web_page_preview=True)
