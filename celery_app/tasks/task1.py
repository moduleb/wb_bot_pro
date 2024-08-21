import logging

from bot_app import text
from shared import parser

from celery_app.run import app

from shared.db_sync.crud import get_all, get_session_local, update_price

SessionLocal = get_session_local()

@app.task
def notify_price_changes():
    db = SessionLocal()
    logging.debug('Check price...')
    try:
        # Получаем все записи из бд
        items = get_all(db)

        for item in items:
            print(f"{item.url}")
            # # Получаем инфо о товаре и парсим прайс
            data = parser.get_data(item.item_id)
            new_price = parser.get_price(data)
            print(new_price)

            # Если цена изменилась, отправляем сообщение и обновляем инфо в бд
            if item.price != new_price:
                msg = text.price_changed.format(
                    old_price=item.price,
                    new_price=new_price,
                    title=item.title
                )
                # bot.send_message(chat_id=item.user_id, text=msg)
                item.price = new_price
                update_price(db, user_id=item.user_id, item_id=item.item_id, new_price=new_price)
                db.close()
                return "DONE"

    except Exception as e:
        logging.error(str(e))

