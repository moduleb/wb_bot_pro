import json
import logging

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from grpc_celery.celery_app import config
from grpc_celery.celery_app.run import app
from shared.db_models import All_
import grpc

from shared.grpc_models.service_pb2 import ItemRequest
from shared.grpc_models.service_pb2_grpc import ParserServiceStub



engine = create_engine(config.DATABASE_URL_SYNC, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def model2dict(item):
    return {key: getattr(item, key) for key in item.__dict__ if not key.startswith('_')}


# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
redis_client = redis.from_url(config.REDIS_CONNECTION_STRING)


@app.task
def add_to_queue(data):
    logging.debug(f"Добавлено в очередь: {data}")

    # Сериализуем словарь в строку JSON
    message = json.dumps(data)

    # Публикуем сообщение в Redis
    redis_client.publish('price_change_channel', message)


@app.task
def notify_price_changes():
    logging.debug('Check price...')

    # Открываем сессию
    db = SessionLocal()

    try:
        # Получаем все записи из бд
        items = db.query(All_).all()

        logging.debug("Получено записей из бд: {}".format(len(items)))

        # Парсим данные товара
        with grpc.insecure_channel(config.GRPC_CONNECTION_STRING) as channel:
            stub = ParserServiceStub(channel)

            for item in items:

                request = ItemRequest(url=item.url)
                item_from_grps = stub.GetItemInfo(request)

                # Получаем инфо о товаре и парсим прайс
                new_price = item_from_grps.price

                # Счетчик товаров, где цена изменилась
                counter = 0

                # Если цена изменилась, отправляем сообщение и обновляем инфо в бд
                if item.price != new_price:
                    counter += 1
                    logging.debug("Изменилась цена на товар: {title}\n"
                                  "Старая цена: {old_price}. Новая цена: {new_price}.".format(
                        title=item_from_grps.title,
                        old_price=item.price,
                        new_price=new_price
                    ))

                    # Преобразовываем все атрибуты модели в словарь
                    # ПОЧЕМУ ТО ЧЕРЕЗ ЭТУ КОНСТРУКЦИЮ НЕ РАБОТАЕТ ИМЕННО В ЗАДАЧЕ, ОТДЕЛЬНО ВСЕ ОК
                    # data = {key: getattr(item, key) for key in item.__dict__ if not key.startswith('_')}
                    # data = model2dict(item)

                    data = {
                        "title": item_from_grps.title,
                        "old_price": item.price,
                        "new_price": new_price,
                        'user_id': item.user_id
                    }

                    add_to_queue.delay(data)

                    # Сохраняем новый прайс
                    item.price = new_price
                    db.commit()

    except Exception as e:
        logging.error(str(e))

    # Закрываем сессию
    db.close()

    return f"Изменен прайс у объектов: {counter}"


