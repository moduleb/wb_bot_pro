from typing import Optional
from urllib.parse import urlparse

import requests


class Item:
    def __init__(self, url, user_id):
        self._base_api_url = 'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={item_id}'
        self._id: int = self._get_id(url)
        self._api_url: str = self._get_api_url()
        data = self._get_data()
        self._price: int = self._get_price(data)
        self.title: str = self._get_title(data)
        self.user_id: int= user_id

    def __str__(self):
        return f'{self.title}, {self.price} руб.'

    def _get_id(self, original_url) -> int:
        # Парсим url и проверяем, что он валидный
        result = urlparse(original_url)
        if not result.scheme and result.netloc:
            raise ValueError

        # Извлекаем id
        path_segments = result.path.split('/')
        if len(path_segments) > 2:
            item_id = path_segments[2]
        else:
            raise ValueError

        # Проверяем валидность id
        id = int(item_id)
        return id

    def _get_data(self) -> dict:
        result = requests.get(url=self._api_url).json()
        if result:
            return result
        else:
            raise ValueError

    def _get_price(self, data=None) -> int:
        if not data:
            data = self._get_data()
        price = data['data']['products'][0]['sizes'][0]['price']['total']
        if not int(price) or price <= 0:
            raise ValueError("Цена недоступна")
        return int(price) // 100

    def _get_title(self, data=None) -> str:
        if not data:
            data = self._get_data()
        title = data['data']['products'][0]['name']
        return title if title else ValueError("Название недоступно")

    def _get_api_url(self):
        api_url = self._base_api_url.format(item_id=self._id)
        return api_url

    def check_price(self) -> Optional[int]:
        new_price = self._get_price()
        if self.price != new_price:
            return new_price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        try:
            if int(price) > 0:
                self._price = price
            else:
                raise ValueError
        except ValueError:
            raise ValueError("Price should be an integer > 0")
