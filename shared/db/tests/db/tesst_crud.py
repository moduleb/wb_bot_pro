import pytest

from bot_app.db import save_one, delete_one, get_many_by_filters, save_many, delete_many
from bot_app.db import create_tables
from bot_app.db.models import TestTable
from bot_app.shared import drop_test_table


@pytest.mark.asyncio
async def test_crud_one_obj(test_objs):

    await drop_test_table()
    await create_tables()

    # Assert SAVING
    await save_one(test_objs[0])
    objs = await get_many_by_filters(model=TestTable, user_name="test_user_name")
    assert objs[0].user_name == test_objs[0].user_name

    # Assert DELETING
    await delete_one(objs[0])
    objs = await get_many_by_filters(model=TestTable, user_name="test_user_name")
    assert objs == []

    await drop_test_table()

@pytest.mark.asyncio
async def test_crud_many_objs(test_objs):

    await drop_test_table()
    await create_tables()

    # Assert SAVING
    await save_many(test_objs)
    objs = await get_many_by_filters(model=TestTable, user_name="test_user_name")
    assert len(objs) == 2

    # Assert DELETING
    await delete_many(objs)
    objs = await get_many_by_filters(model=TestTable, user_name="test_user_name")
    assert objs == []

    await drop_test_table()