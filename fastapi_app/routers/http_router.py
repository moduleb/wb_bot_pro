import json
import logging
from typing import List

import asyncpg

from fastapi import APIRouter

from db import service
from models.all_ import AllItem
from fastapi import status, HTTPException

from parser_func import parser

router = APIRouter()

logging.basicConfig(level=logging.INFO)


@router.get("/", response_model=List[AllItem], status_code=status.HTTP_200_OK)
async def get_all(user_id):
    data = await service.get_items_by_user_id(user_id)
    return data


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(user_id, url):
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

    except asyncpg.InterfaceError as e:
        logging.error("База данных недоступна.\n Error: {}".format(e))
        return HTTPException(status_code=500,
                             detail="База данных недоступна.\n Error: {}".format(e))


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id, item_id):
    await service.delete(user_id=user_id, item_id=item_id)
