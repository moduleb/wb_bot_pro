import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from app.bot import bot
from app.handlers import router

dp = Dispatcher(storage=MemoryStorage())


async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, "hello")
    await message.reply("hello")
    await message.answer("hello")



async def main():
    # url = 'https://www.wildberries.ru/catalog/180400996/detail.aspx'
    # delay = 2
    # await check_price(url, delay)

    # Создаем бота

    dp.include_router(router)
    # dp.message.register(get_start)
    dp.message.middleware(ChatActionMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
