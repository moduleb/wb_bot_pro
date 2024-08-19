import pytest

from db.models import Base, TestTable

from db.database import engine, create_tables


async def drop_test_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all, tables=[TestTable.__table__])


@pytest.fixture(scope='class', autouse=True)
async def setup_database():
    # Удаляем таблицы, если они существуют
    await drop_test_table()
    # Создаем таблицы
    await create_tables()
    yield  # Здесь выполняются тесты
    # Удаляем таблицы после всех тестов в классе
    await drop_test_table()


@pytest.fixture
def test_objs():
    test_obj1 = TestTable(user_name="test_user_name")
    test_obj2 = TestTable(user_name="test_user_name")
    return [test_obj1, test_obj2]
