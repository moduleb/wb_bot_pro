import pytest

from app.utils import get_item_id, get_title, get_price




def test_get_item_id():

    # неверный url
    url = "sdg"
    with pytest.raises(ValueError):
        get_item_id(url)

    # неверный url со слешами
    url = "asdg/sdf/sadf"
    with pytest.raises(ValueError):
        get_item_id(url)

    # текст вместо id
    url = 'https://www.wildberries.ru/catalog/aaa/detail.aspx'
    with pytest.raises(ValueError):
        get_item_id(url)

def test_get_title():
    data = {"Sdgsg": "sdfs"}
    with pytest.raises(KeyError):
        get_title(data)

def test_get_price():
    data = {"Sdgsg": "sdfs"}
    with pytest.raises(KeyError):
        get_price(data)

    ValueError
    with pytest.raises(KeyError):
        get_price(data)