# db/session.py
import logging
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from .database import AsyncSessionLocal

class DB_error(BaseException):
    pass

def async_session_scope(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with AsyncSessionLocal() as session:
            try:
                result = await func(session, *args, **kwargs)
                await session.commit()
                return result
            except ValueError:
                pass
            # except SQLAlchemyError as e:
            #     await session.rollback()
            #     logging.error(f"Error occurred: {e}")
            #     return None
            # except OSError as e:
            #     logging.error("Ошибка подключения к базе данных: {}".format(e))
            #     raise DB_error("База данных недоступна") from e
    return wrapper
