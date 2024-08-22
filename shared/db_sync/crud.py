# db/crud.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.db.config import DATABASE_URL_SYNC

def get_session_local():
    engine = create_engine(DATABASE_URL_SYNC, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal


