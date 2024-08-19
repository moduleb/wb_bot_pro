# main.py
import asyncio

from db.database import create_tables


async def main():
    # Создание базы данных
    await create_tables()

    # # Проверка соединения
    # async with AsyncSessionLocal() as session:
    #     try:
    #         await session.execute("SELECT 1")
    #         print("Соединение с базой данных установлено.")
    #     except Exception as e:
    #         print(f"Ошибка соединения с базой данных: {e}")
    #         return

    # Добавление нового элемента
    # result = await add_item("44user_name", "12", 12, 12, "title", "url")
    # print(result)
    # obj = All_(
    #     user_name="user_name",
    #     user_host="user_host",
    #     item_id=54,
    #     price=54,
    #     title="title",
    #     url="url"
    # )
    # # await save(obj)
    # items = await get_many_by_filters(model=All_, user_name="44user_name")
    # # await delete_many(items)


if __name__ == "__main__":
    asyncio.run(main())
