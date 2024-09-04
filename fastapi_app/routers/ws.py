import json
import logging

import asyncpg

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from db import service
from parser_func import parser

from routers import http_router

connections = []

router = APIRouter()

logging.basicConfig(level=logging.INFO)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            message_dict = json.loads(data)

            action = message_dict.get("action")
            user_id = message_dict.get("user_id")

            if action == "get_all":

                # data = await service.get_items_by_user_id(user_id)
                data = await http_router.get_all(user_id)

                keys = {"url", "price", "title", "item_id"}
                data_to_send = [
                    {key: getattr(item, key) for key in keys if hasattr(item, key)}
                    for item in data
                ]

                message_dict = {
                    "success": True,
                    "data": data_to_send
                }

                message_json = json.dumps(message_dict)

                await websocket.send_text(message_json)

            elif action == "delete":
                item_id = message_dict.get("item_id")

                await service.delete(user_id=user_id, item_id=item_id)

                message_dict = {"success": True}
                message_json = json.dumps(message_dict)

                await websocket.send_text(message_json)

            elif action == "create":
                url = message_dict.get("url")
                user_id = message_dict.get("user_id")

                data = await parser(url)
                price = data.get("price")
                title = data.get("title")
                item_id = data.get("item_id")

                try:
                    # Сохраняем в бд
                    await service.insert(user_id=user_id,
                                         item_id=item_id,
                                         price=price,
                                         title=title,
                                         url=url)

                    message_dict = {"success": True}

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
