import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from . import crud, config
from shared.db_models import All_, Base

logging.info(config.DATABASE_URL)
# Создание асинхронного движка
engine = create_async_engine(config.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def insert(user_id, item_id, price, title, url) -> None:
    obj = All_(user_id=int(user_id),
               item_id=int(item_id),
               price=int(price),
               title=str(title),
               url=str(url)
               )
    print("insert", obj)

    async with AsyncSessionLocal() as session:
        await crud.save_one(session, obj)


async def get_item_by_user_id_and_item_id(user_id, item_id):
    async with AsyncSessionLocal() as session:
        objs = await crud.get_many_by_filters(session, model=All_,
                                              user_id=int(user_id),
                                              item_id=int(item_id))
    return objs[0] if objs else []


async def get_items_by_user_id(user_id):
    async with AsyncSessionLocal() as session:
        objs = await crud.get_many_by_filters(session, model=All_, user_id=int(user_id))
    return objs


async def get_all():
    async with AsyncSessionLocal() as session:
        objs = await crud.get_many_by_filters(session, model=All_)
    return objs


async def delete(user_id, item_id) -> None:
    async with AsyncSessionLocal() as session:
        obj = await get_item_by_user_id_and_item_id(int(user_id), int(item_id))
    await crud.delete_one(session, obj)
