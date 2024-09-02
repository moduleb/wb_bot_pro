import json
import logging
import os

import asyncpg

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from db import service

connections = []

for key, value in os.environ.items():
    print(f"{key}={value}")

router = APIRouter()

logging.basicConfig(level=logging.INFO)
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
            price = message_dict.get("price")
            title = message_dict.get("title")
            url = message_dict.get("url")

            if action == "get_all":

                data = await service.get_items_by_user_id(user_id)
                data_to_send = []
                # logging.info(message_dict)
                # data_to_send = [{
                #     "url": "url",
                #     "price": "200",
                #     "title": "title",
                #     "item_id": "item_id"
                # }]
                for item in data:
                    data_to_send.append({
                        "url": item.url,
                        "price": item.price,
                        "title": item.title,
                        "item_id": item.item_id
                    })

                message_dict = {
                    "success": True,
                    "data": data_to_send
                }

                message_json = json.dumps(message_dict)

                await websocket.send_text(message_json)


            elif action == "delete":

                await service.delete(user_id=user_id,
                                     item_id=item_id)
                message_dict = {
                    "success": True
                }
                message_json = json.dumps(message_dict)

                await websocket.send_text(message_json)

            elif action == "create":
                try:
                    # Сохраняем в бд
                    await service.insert(user_id=user_id,
                                         item_id=item_id,
                                         price=price,
                                         title=title,
                                         url=url)

                    message_dict = {
                        "success": True
                    }

                except asyncpg.InterfaceError as e:
                    message_dict = {
                        "success": False,
                        "message": "База данных недоступна.\n Error: {}".format(e)
                    }

                message_json = json.dumps(message_dict)
                await websocket.send_text(message_json)

            else:
                message_dict = {
                    "success": False,
                    "message": "Операция не поддерживается: {}".format(action)
                }
                message_json = json.dumps(message_dict)
                await websocket.send_text(message_json)


    except WebSocketDisconnect:
        connections.remove(websocket)

    except Exception as e:
        logging.error(f"Error: {e}")
        message_dict = {
            "success": False,
            "message": "Неизвестная ошибка: {}".format(e)
        }
        message_json = json.dumps(message_dict)
        await websocket.send_text(message_json)
