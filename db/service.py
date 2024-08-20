from db import crud
from db.models import All_


async def insert(user_id, item_id, price, title, url) -> None:
    obj = All_(user_id=user_id,
               item_id=item_id,
               price=price,
               title=title,
               url=url
    )
    await crud.save_one(obj)

async def get_item_by_user_id_and_item_id(user_id, item_id):
    objs = await crud.get_many_by_filters(model=All_,
                                          user_id=int(user_id),
                                          item_id=int(item_id))
    return objs[0] if objs else []


async def get_items_by_user_id(user_id):
    objs = await crud.get_many_by_filters(model=All_, user_id=user_id)
    return objs

async def delete(user_id, item_id) -> None:
    obj = await get_item_by_user_id_and_item_id(int(user_id), int(item_id))
    await crud.delete_one(obj)