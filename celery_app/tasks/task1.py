import logging

from bot_app import db, parser, text

from main import bot
from ..celery_config import app


@app.task()
def notify_price_changes():
    logging.debug('Check price...')
    try:
        # Получаем все записи из бд
        items = db.get_all()

        for item in items:

            # Получаем инфо о товаре и парсим прайс
            data = parser.get_data(item.item_id)
            new_price = parser.get_price(data)

            # Если цена изменилась, отправляем сообщение и обновляем инфо в бд
            if item.price != new_price:
                msg = text.price_changed.format(
                    old_price=item.price,
                    new_price=new_price,
                    title=item.title
                )
                bot.send_message(chat_id=item.user_id, text=msg)
                item.price = new_price
                db.update_price(id_=item.id, price=item.price)

    except Exception as e:
        logging.error(str(e))

