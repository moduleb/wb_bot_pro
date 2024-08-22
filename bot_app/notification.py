msg = text.price_changed.format(
    old_price=item.price,
    new_price=new_price,
    title=item.title
)

import redis
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = 'YOUR_API_TOKEN'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

async def listen_price_changes():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('price_change_channel')

    for message in pubsub.listen():
        if message['type'] == 'message':
            # Десериализуем сообщение из JSON
            data = json.loads(message['data'])
            # Обработка данных и отправка уведомления
            await bot.send_message(data['user_id'],
                f"Цена товара '{data['name']}' изменилась с {data['old_price']} на {data['new_price']}.")

@dp.on_startup
async def on_startup(dp):
    asyncio.create_task(listen_price_changes())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
