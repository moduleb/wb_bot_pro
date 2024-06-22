import sqlite3
from dataclasses import dataclass

from app import config


@dataclass
class Item:
    id: int
    user_id: int
    item_id: int
    price: int
    title: str
    url: str

    def to_tuple(self):
        return (self.user_id, self.item_id, self.price, self.title, self.url)


conn = sqlite3.connect(config.sql_connect_string)
cursor = conn.cursor()
table_name = 'test'
query = "create table IF NOT EXISTS %s (\
    id integer primary key autoincrement,\
    user_id integer,\
    item_id integer,\
    price integer,\
    title varchar(100),\
    url varchar(100)\
    )" % table_name

cursor.execute(query)
conn.commit()

def insert(user_id, item_id, price, title, url):
    ins = "insert into %s (user_id, item_id, price, title, url) values (?, ?, ?, ?, ?)" % table_name
    cursor.execute(ins, (user_id, item_id, price, title, url))
    created_id = cursor.lastrowid
    conn.commit()
    return created_id


def update_price(id_, price):
    ins = f"update {table_name} set price = ? where id = ?"
    cursor.execute(ins, (price, id_))
    conn.commit()
    return cursor.rowcount


def get_item_by_id(id_):
    query = 'select * from %s where id = %d' % (table_name, id_)
    row = cursor.execute(query).fetchone()
    return __convert_db_data_to_objs(row)


def get_items_by_user_id_and_item_id(user_id, item_id):
    query = f'select * from {table_name} where user_id = {user_id} and item_id = {item_id}'
    row = cursor.execute(query).fetchall()
    return __convert_db_data_to_objs(row)


def get_items_by_user_id(user_id):
    query = 'select * from %s where user_id = %d' % (table_name, user_id)
    rows = cursor.execute(query).fetchall()
    return __convert_db_data_to_objs(rows)


def get_all():
    query = 'select * from %s' % table_name
    rows = cursor.execute(query).fetchall()
    return __convert_db_data_to_objs(rows)


def __convert_db_data_to_objs(rows):
    return [Item(*row) for row in rows] if isinstance(rows, list) else Item(*rows)


def delete(user_id, item_id):
    query = f'DELETE FROM {table_name} WHERE user_id = ? AND item_id = ?'
    cursor.execute(query, (user_id, item_id))
    conn.commit()
    return cursor.rowcount


def delete_by_id(id_):
    query = f'DELETE FROM {table_name} WHERE id = ?'
    cursor.execute(query, (id_,))
    conn.commit()
    return cursor.rowcount
