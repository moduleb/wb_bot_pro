
import grpc

from proto.service_pb2 import ItemRequest
from proto.service_pb2_grpc import ParserServiceStub
from config import GRPC_CONNECTION_STRING


# Парсим данные товара
async def parser(url):
    async with grpc.aio.insecure_channel(GRPC_CONNECTION_STRING) as channel:
        stub = ParserServiceStub(channel)

        # url = "https://www.wildberries.ru/catalog/210331544/detail.aspx"
        request = ItemRequest(url=url)
        item = await stub.GetItemInfo(request)

        """ Формат ответа от сервера
        ItemResponse {
        string title = 1; // Название элемента
        float price = 2; // Цена элемента   
        }
        """

        return {
            "title": item.title,
            "price": item.price,
            "item_id": item.item_id
        }