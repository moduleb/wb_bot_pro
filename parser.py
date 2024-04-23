import asyncio
from dataclasses import dataclass

import requests

from messages import price_changed, price_unchanged
from send_msg import send_msg


@dataclass
class Item:
    price: int
    title: str

def get_url_for_api(url):
    # url = https://www.wildberries.ru/catalog/180400996/detail.aspx
    item_id = url.split('/')[-2]
    url = f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={item_id}'
    return url

def get_data(url: str) -> dict:
    result = requests.get(url=url)
    return result.json()


def get_price(data: dict) -> int:
    price = data['data']['products'][0]['sizes'][0]['price']['total']
    return int(price / 100) if price else Exception("Цена недоступна")


def get_title(data: dict) -> str:
    title = data['data']['products'][0]['name']
    return title if title else Exception("Название недоступно")


async def check_price(original_url, delay):
    """
    1. Получаем инфо о товаре
    2. Через каждые {delay} секунд обновляем информацию и сравниваем с ранее полученной
    3. Если цена изменилась отправляем сообщение
    4. Устанавливаем новое инфо как текущее и далее сравниваем уже с ним
    """
    url = get_url_for_api(original_url)
    data = get_data(url)
    item = Item(price=get_price(data),
                title=get_title(data))
    while True:
        new_data = get_data(url)
        new_price = get_price(new_data)

        if item.price != new_price:
            msg = price_changed.format(
                title=item.title,
                old_price=item.price,
                new_price=new_price
            )
            send_msg(msg)
            item.price = new_price
        else:
            msg = price_unchanged.format(
                title=item.title,
                price=item.price,
            )
            send_msg(msg)
        await asyncio.sleep(delay)
