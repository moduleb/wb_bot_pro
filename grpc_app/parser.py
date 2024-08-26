from urllib.parse import urlparse

import requests


class ParserError(Exception):
    pass


def get_item_info(url: str):
    item_id = _get_item_id(url)
    data = _get_data(item_id)
    price = _get_price(data)
    title = _get_title(data)
    return {
        "price": price,
        "title": title,
        "item_id": item_id
    }


def _get_item_id(url):
    try:
        result = urlparse(url)
        if result.scheme != 'https' or result.netloc != 'www.wildberries.ru':
            raise ParserError("Ссылка должна начинаться с https://www.wildberries.ru/")

        path_segments = result.path.split('/')
        if len(path_segments) <= 2:
            raise ParserError("URL не является ссылкой на конкретный товар")

        return int(path_segments[2])

    except (ValueError, IndexError) as e:
        raise ParserError("Неправильный формат id") from e


def _get_data(item_id) -> dict:
    base_url = 'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={item_id}'

    api_url = base_url.format(item_id=item_id)

    if result := requests.get(url=api_url).json():
        return result
    else:
        raise ParserError('Данные не получены')


def _get_price(data):
    try:
        price = data['data']['products'][0]['sizes'][0]['price']['total']

        if price <= 0:
            raise ValueError(f'Полученный price <= 0: {price}')

    except IndexError as e:  # формат данных в словаре не совпадает с ожидаемым
        raise ParserError('Неверная ссылка') from e

    except Exception as e:
        raise ParserError('Невозможно получить информацию о товаре') from e

    else:
        return int(price) // 100


def _get_title(data):
    try:
        return data['data']['products'][0]['name']
    except Exception as e:
        raise ParserError('Неверная ссылка') from e
