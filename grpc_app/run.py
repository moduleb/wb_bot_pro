import os
from concurrent import futures

import grpc

from grpc_app import parser
from shared.grpc_models.service_pb2 import ItemResponse, ItemRequest
from shared.grpc_models.service_pb2_grpc import ParserServiceServicer, add_ParserServiceServicer_to_server

# Установка переменных окружения
os.environ['GRPC_VERBOSITY'] = 'DEBUG'
# os.environ['GRPC_TRACE'] = 'all'
# os.environ['GRPC_TRACE'] = 'client,server,message'  # Отображение только вызовов и сообщений

class ParserService(ParserServiceServicer):
    def GetItemInfo(self, request: ItemRequest, context):
        """ Формат request
        ItemRequest {
        string url = 1;
        }
        """

        data = parser.get_item_info(request.url)

        # Возвращаем ответ с названием и ценой
        return ItemResponse(
            title=data.get("title"),
            price=data.get("price")

        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ParserServiceServicer_to_server(ParserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051...")
    server.wait_for_termination()  # Ожидание завершения работы сервера


if __name__ == '__main__':
    serve()
