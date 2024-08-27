import asyncio
import json

from bot_app import text


async def listen_price_changes(bot, redis_client):
    print("listen_price_changes")
    pubsub = redis_client.pubsub()
    await pubsub.subscribe('price_change_channel')

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message and message['type'] == 'message':
                data = json.loads(message['data'])

                # Формируем сообщение
                msg = text.price_changed.format(
                    old_price=data['old_price'],
                    new_price=data['new_price'],
                    title=data['title']
                )

                user_id = data['user_id']

                # Отправка уведомления
                await bot.send_message(user_id, msg)

            await asyncio.sleep(0.1)  # Небольшая пауза, чтобы избежать излишней загрузки CPU

    except Exception as e:
        print(f"Error while listening for messages: {e}")
    finally:
        await pubsub.unsubscribe('price_change_channel')
        print("Unsubscribed from channel and exiting listen_price_changes.")