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

import redis.asyncio as aioredis
from aiogram import Dispatcher, types, Bot
from aiogram.fsm.storage.memory import MemoryStorage

import config
from ws import ws_manager

from handlers import router
from notification import listen_price_changes

commands = [
    types.BotCommand(command="/start", description="Начать диалог"),
    types.BotCommand(command="/tasks", description="Мои отслеживания..."),
]

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=config.TOKEN)

# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

async def main():
    dp.include_router(router)
    # await create_tables()
    redis_client = await aioredis.from_url("redis://localhost")
    await bot.set_my_commands(commands)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        task = asyncio.create_task(listen_price_changes(bot, redis_client))
        # await ws_manager.connect()

        # Запускаем бот
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(),
                               close_bot_session=True)
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    finally:
        task.cancel()
        await ws_manager.close()
        logging.info("Бот остановлен")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
