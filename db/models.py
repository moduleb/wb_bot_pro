from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

from alchemy import engine

Base = declarative_base()


class All_(Base):
    __tablename__ = 'all_'

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_host = Column(String)
    item_id = Column(Integer)
    price = Column(Integer)
    title = Column(String)
    url = Column(String)



Base.metadata.create_all(engine)
