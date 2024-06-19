from unittest.mock import AsyncMock

import pytest
from aiogram import Bot

from app import db, config
from app.parser import get_item_id, get_data, get_price, get_title
from app.scheduler import notify_price_changes

urls = ('sdg',
        "asdg/sdf/sadf",
        "https://www.wildberries.ru/",  # без параметров
        "http://www.wildberries.ru/asdf/23424/23423424",  # http вместо https
        "https://www.wildb3erries.ru/23424/234234",  # ошибка в имени сайта
        "https://www.wildb3erries.ru/sgswg/sdf",  # буквы вместо id
        )


@pytest.mark.parametrize("url", urls)
def test_get_item_id(url):
    from app.parser import ParserError, get_item_id
    with pytest.raises(ParserError):
        get_item_id(url)


def test_parser():
    url = "https://www.wildberries.ru/catalog/208992438/detail.aspx"
    item_id = get_item_id(url)
    assert int(item_id), "ID не получено"
    data = get_data(item_id)
    assert isinstance(data, dict), "Data не получено"
    price = get_price(data)
    assert int(price), "Price не получено"
    title = get_title(data)
    assert isinstance(title, str), "Title не получено"


def test_db():
    user_id = 1
    item_id = 2
    price = 3
    title = '444'

    # Insert
    created_id = db.insert(user_id, item_id, price, title)
    item = db.get_item_by_id(created_id)
    assert isinstance(item, db.Item) is True
    assert item.to_tuple() == (user_id, item_id, price, title)

    # Update
    price = 8767
    item.price = price
    db.update_price(id_=item.id, price=item.price)
    item = db.get_item_by_id(created_id)
    assert item.to_tuple() == (user_id, item_id, price, title)
    assert db.delete_by_id(created_id) == 1


@pytest.mark.asyncio
async def test_notify_price_changes():
    url = "https://www.wildberries.ru/catalog/208992438/detail.aspx"
    item_id = get_item_id(url)
    user_id = config.admin_tg_id
    price = 1
    title = "title"

    # Создаем запись в бд с фейковыми данными, кроме item_id
    created_id = db.insert(user_id, item_id, price, title)
    assert created_id > 0

    # Проверяем, что запустилась функция отправки уведомления об изменении цены
    bot = AsyncMock()
    await notify_price_changes(bot)
    bot.send_message.assert_called_once()

    # Проверяем, что бот отправил сообщение об изменении цены
    # Изменяем цену на несуществующую, чтобы функция сработала
    bot = Bot(token=config.TOKEN)
    db.update_price(id_=created_id, price=price)
    await notify_price_changes(bot)

    # Проверяем что обновился price в бд
    updated_item = db.get_item_by_id(created_id)
    assert updated_item.price != price

    # Удаляем запись в бд
    assert db.delete_by_id(created_id) == 1

