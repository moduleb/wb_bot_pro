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

from bot_app import config
from bot_app.bot_.handlers import router
from bot_app.db import cursor, conn

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
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(),
                               close_bot_session=True)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())



