# db/crud.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from shared.db.config import DATABASE_URL_SYNC
from shared.db.models import All_

def get_session_local():
    engine = create_engine(DATABASE_URL_SYNC, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

def get_all(db: Session):
    return db.query(All_).all()

def update_price(db: Session, user_id: int, item_id: int, new_price: int):
    item = db.query(All_).filter(All_.user_id == user_id, All_.item_id == item_id).one()
    item.price = new_price
    db.commit()
