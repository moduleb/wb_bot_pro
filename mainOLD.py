"""
    bot.delete_webhook(drop_pending_updates=True)
Dы указываете боту удалить текущий вебхук.
Параметр drop_pending_updates=True указывает боту также удалить все ожидающие обновления,
которые могли быть накоплены во время использования вебхука.

    dp.start_polling(bot) запускает бота с использованием метода Long Polling.
+ allowed_updates=dp.resolve_used_update_types() указывает, какие типы обновлений бот будет получать.
бот будет ограничивать типы обновлений, которые он получает, только теми, которые он может обработать,
что может быть полезно для оптимизации работы бота и уменьшения нагрузки на сервер.
"""
import asyncio
import logging

from aiogram import Dispatcher, types, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from app import config
from app.bot_.handlers import router
from app.db import cursor, conn
from app.scheduler import loop_check_price

commands = [
    types.BotCommand(command="/start", description="Начать диалог"),
    types.BotCommand(command="/tasks", description="Мои отслеживания..."),
]

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=config.TOKEN)


async def main():
    dp.include_router(router)
    await bot.set_my_commands(commands)
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await asyncio.gather(
            dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()),
            loop_check_price(timeout=config.timeout, bot=bot)
        )
    finally:
        await bot.session.close()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
