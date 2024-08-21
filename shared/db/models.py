# db/models.py

from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import DeclarativeBase


# Base = declarative_base()
class Base(DeclarativeBase):
    pass


class All_(Base):
    __tablename__ = 'all_'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    item_id = Column(BigInteger)
    price = Column(Integer)
    title = Column(String)
    url = Column(String)


# class TestTable(Base):
#     __tablename__ = 'test_table'
#
#     id = Column(Integer, primary_key=True)
#     user_name = Column(String)
