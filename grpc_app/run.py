import logging

from concurrent import futures

import grpc

import parser
from shared.grpc_models.service_pb2 import ItemResponse, ItemRequest
from shared.grpc_models.service_pb2_grpc import ParserServiceServicer, add_ParserServiceServicer_to_server

# Установка переменных окружения
# os.environ['GRPC_VERBOSITY'] = 'DEBUG'
# os.environ['GRPC_TRACE'] = 'all'
# os.environ['GRPC_TRACE'] = 'client,server,message'  # Отображение только вызовов и сообщений
import signal
import sys



class ParserService(ParserServiceServicer):
    def GetItemInfo(self, request: ItemRequest, context):

        logging.info("GetItemInfo func started...")
        """ Формат request
        
        ItemRequest {
        string url = 1;
        }
        """
        logging.info("Принят request.url: {}".format(request.url))

        data = parser.get_item_info(request.url)
        logging.info("От парсера получена data")

        # Возвращаем ответ с названием и ценой
        return ItemResponse(
            title=data.get("title"),
            price=data.get("price"),
            item_id=data.get("item_id")
        )


def signal_handler(server):
    logging.info("Received signal to terminate. Shutting down...")
    server.stop(0)  # Остановить сервер
    sys.exit(0)

def serve():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Добавьте ваш gRPC сервис
    add_ParserServiceServicer_to_server(ParserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Server is running on port 50051...")

    # Обработка сигналов
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(server))
    signal.signal(signal.SIGTERM, lambda sig, frame: signal_handler(server))

    server.wait_for_termination()  # Ожидание завершения работы сервера

if __name__ == '__main__':
    serve()
