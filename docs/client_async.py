import grpc
import asyncio

from grpc_app.proto.service_pb2 import ItemRequest
from grpc_app.proto.service_pb2_grpc import ParserServiceStub
from config import GRPC_CONNECTION_STRING
# GRPC_CONNECTION_STRING = 'localhost:50051'

url = "https://www.wildberries.ru/catalog/210331544/detail.aspx"


async def run():
    async with grpc.aio.insecure_channel(GRPC_CONNECTION_STRING) as channel:
        stub = ParserServiceStub(channel)

        request = ItemRequest(url=url)
        item = await stub.GetItemInfo(request)

        """
        ItemResponse {
        string title = 1; // Название элемента
        float price = 2; // Цена элемента   
        }
        """

        print("Client received Item:")
        print(f"Title: {item.title}")
        print(f"Price: {item.price}")


if __name__ == '__main__':
    asyncio.run(run())
