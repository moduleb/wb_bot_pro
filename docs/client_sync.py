import grpc

from service_pb2 import ItemRequest
from service_pb2_grpc import ParserServiceStub

GRPC_CONNECTION_STRING = 'localhost:50051'

url = "https://www.wildberries.ru/catalog/210331544/detail.aspx"

def run():
    with grpc.insecure_channel(GRPC_CONNECTION_STRING) as channel:
        stub = ParserServiceStub(channel)

        request = ItemRequest(url=url)
        item = stub.GetItemInfo(request)
        print("Client received Item:")
        print(f"Title: {item.title}")
        print(f"Price: {item.price}")


if __name__ == '__main__':
    run()
