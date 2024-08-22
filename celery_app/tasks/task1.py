import json
import logging

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from celery_app.run import app
from shared import parser
from shared.db.config import DATABASE_URL_SYNC
from shared.db.models import All_

engine = create_engine(DATABASE_URL_SYNC, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def model2dict(item):
    return {key: getattr(item, key) for key in item.__dict__ if not key.startswith('_')}

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.task
def add_to_queue(data):
    print(f"Добавлено в очередь: {data}")

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

        for item in items:

            # Получаем инфо о товаре и парсим прайс
            data = parser.get_data(item.item_id)
            new_price = parser.get_price(data)

            # Счетчик товаров, где цена изменилась
            counter = 0

            # Если цена изменилась, отправляем сообщение и обновляем инфо в бд
            if item.price != new_price:
                counter +=1
                logging.debug("Изменилась цена на товар: {title}\n"
                              "Старая цена: {old_price}. Новая цена: {new_price}.".format(
                    title=item.title,
                    old_price=item.price,
                    new_price=new_price
                ))



                # Преобразовываем все атрибуты модели в словарь
                # ПОЧЕМУ ТО ЧЕРЕЗ ЭТУ КОНСТРУКЦИЮ НЕ РАБОТАЕТ ИМЕННО В ЗАДАЧЕ, ОТДЕЛЬНО ВСЕ ОК
                # data = {key: getattr(item, key) for key in item.__dict__ if not key.startswith('_')}
                # data = model2dict(item)

                data = {
                    "title":item.title,
                    "old_price": item.price,
                    "new_price": new_price
                }

                add_to_queue.delay(data)

                # Сохраняем новый прайс
                item.price = new_price
                db.commit()

                # Закрываем сессию
                db.close()



                return f"Изменен прайс у объектов: {counter}"


    except Exception as e:
        logging.error(str(e))

#
# db = SessionLocal()
# items = db.query(All_).all()
# item = items[0]
#
#
#
# data = model2dict(item)
# print(data)