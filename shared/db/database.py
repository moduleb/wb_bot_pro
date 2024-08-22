# db/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Base
from . import config

# Создание асинхронного движка
#
# engine = create_async_engine(config.DATABASE_URL, echo=True)
# AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
#
#
# async def create_tables(engine):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
