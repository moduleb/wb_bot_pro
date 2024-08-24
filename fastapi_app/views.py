# Хранение активных соединений
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

            # Отправка ответа
            await websocket.send_text(f"Message from client: {data}")

    except WebSocketDisconnect:
        connections.remove(websocket)

    except Exception as e:
        logging.error(f"Error: {e}")