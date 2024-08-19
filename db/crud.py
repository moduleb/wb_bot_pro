# db/crud.py
import logging
from typing import List, TypeVar, Dict

from sqlalchemy.future import select

from .database import AsyncSession
from .models import Base
from .session import async_session_scope


# ----- CREATE -----
@async_session_scope
async def save_one(session: AsyncSession, obj) -> None:
    """Сохраняет объект в базу данных"""
    session.add(obj)


@async_session_scope
async def save_many(session: AsyncSession, objs: List[object]) -> None:
    """Сохраняет объекты в базу данных"""
    session.add_all(objs)


# ----- READ -----

# Определяем тип переменной для модели
M = TypeVar('M', bound=Base)


@async_session_scope
async def get_many_by_filters(
        session: AsyncSession, model: M, **filters: Dict[str, str|int]) -> list[M]:
    # Начинаем строить запрос
    query = select(model)

    # Применяем фильтры
    for key, value in filters.items():
        if hasattr(model, key):
            query = query.where(getattr(model, key) == value)
        else:
            logging.debug("Invalid filter key: {}. No such attribute in model: {}".format(key, model))

    # Выполняем запрос
    result = await session.execute(query)
    return list(result.scalars().all())


# ----- DELETE -----
@async_session_scope
async def delete_one(session: AsyncSession, obj) -> None:
    """Удаляет объект из базы данных"""
    await session.delete(obj)


@async_session_scope
async def delete_many(session: AsyncSession, objs: List[object]) -> None:
    """Удаляет объекты из базы данных"""
    # Удаляем каждый объект из сессии
    for obj in objs:
        await session.delete(obj)
