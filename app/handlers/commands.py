from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app import kb, text

router = Router()


# await state.clear()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)




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
