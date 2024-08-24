import asyncio
import websockets
import logging

from bot_app import config


class WebSocketManager:
    def __init__(self, url):
        self.url = url
        self.websocket = None

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.url)
            logging.info("WebSocket connection established.")
        except Exception as e:
            logging.error(f"Failed to connect to WebSocket: {e}")

    async def send(self, message: str):
        for attempt in range(5):
            try:
                if self.websocket is None:
                    await self.connect()  # Пытаемся подключиться, если соединение отсутствует

                await self.websocket.send(message)
                response = await self.websocket.recv()
                logging.info(f"Response from server: {response}")
                return  # Успешная отправка, выходим из метода

            except (websockets.ConnectionClosed, websockets.InvalidStatusCode) as e:
                logging.warning(f"WebSocket connection error: {e}. Attempting to reconnect...")
                await self.connect()  # Пытаемся переподключиться

            except Exception as e:
                logging.error(f"WebSocket error: {e}")

            await asyncio.sleep(2)  # Задержка перед следующей попыткой

        logging.error("Failed to send message after 5 attempts.")

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            logging.info("WebSocket connection closed.")

# Создание экземпляра WebSocketManager
ws_manager = WebSocketManager(config.WS_URL)
