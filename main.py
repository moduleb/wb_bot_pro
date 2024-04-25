import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from app.bot import bot
from app.handlers.commands import router as main_router
from app.handlers.start_task import router as start_task_router
from app.handlers.stop_task import router as stop_task_router

dp = Dispatcher(storage=MemoryStorage())


async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, "hello")
    await message.reply("hello")
    await message.answer("hello")



async def main():

    dp.include_router(main_router)
    dp.include_router(start_task_router)
    dp.include_router(stop_task_router)
    # dp.message.register(get_start)
    # dp.message.middleware(ChatActionMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
