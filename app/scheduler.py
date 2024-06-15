import asyncio
import logging

from app import db, parser, text
from app.bot_.bot import bot


async def notify_price_changes(bot):
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
            await bot.send_message(chat_id=item.user_id, text=msg)
            item.price = new_price
            db.update_price(id_=item.id, price=item.price)


async def loop_check_price(timer):
    while True:

        logging.debug('check price...')

        try:
            await notify_price_changes(bot=bot)
        except Exception as e:
            logging.error(str(e))

        await asyncio.sleep(timer)
