# Хранение активных соединений
import json
import logging

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect


connections = []

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            message_dict = json.loads(data)  # Десериализуем JSON в словарь

            action = message_dict.get("action")
            item_id = message_dict.get("item_id")
            user_id = message_dict.get("user_id")

            # Обработка сообщения
            if action == "get_all":

                # Логика для получения всех записей для user_id
                await websocket.send_text(f"Получены записи для user_id {user_id}")

                data = {"user_id": user_id,
                        "price": 20}

                message = {
                    "success":True,
                    "data":data
                }

                await websocket.send_text(json.dumps(message))

            elif action == "delete":
                # Логика для удаления записи с item_id
                await websocket.send_text(f"Удалена запись с item_id {item_id} для user_id {user_id}")

    except WebSocketDisconnect:
        connections.remove(websocket)

    except Exception as e:
        logging.error(f"Error: {e}")