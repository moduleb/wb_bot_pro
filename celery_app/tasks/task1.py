import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from celery_app.run import app
from shared import parser
from shared.db.config import DATABASE_URL_SYNC
from shared.db.models import All_

engine = create_engine(DATABASE_URL_SYNC, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

                # Сохраняем новый прайс
                item.price = new_price
                db.commit()

                # Закрываем сессию
                db.close()

                # redis.добавить item в очередь

                return f"Изменен прайс у объектов: {counter}"


    except Exception as e:
        logging.error(str(e))
