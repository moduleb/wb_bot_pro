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

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app import config
from app.bot_.bot import bot
from app.bot_.handlers import router
from app.db import cursor, conn
from app.scheduler import loop_check_price

dp = Dispatcher(storage=MemoryStorage())


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await asyncio.gather(
            dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()),
            loop_check_price(timer=config.timeout)
        )

    finally:
        cursor.close()
        conn.close()
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
