import json

from bot_app import text


async def listen_price_changes(bot, redis_client):
    # Подписка на канал
    pubsub = redis_client.pubsub()
    pubsub.subscribe('price_change_channel')

    # Слушаем Redis
    for message in pubsub.listen():
        if message['type'] == 'message':
            # Десериализуем сообщение из JSON
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
