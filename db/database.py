from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from models import All_

# Создание движка
engine = create_engine('postgresql://user:passw53@localhost/db53')
Session = sessionmaker(bind=engine)
session = Session()

# Проверка соединения
try:
    # Попробуем выполнить простой запрос, чтобы проверить соединение
    session.execute(text("SELECT 1"))
    print("Соединение с базой данных установлено.")
except Exception as e:
    print(f"Ошибка соединения с базой данных: {e}")
    session.close()
    exit(1)  # Завершить программу, если соединение не удалось

# Пример добавления пользователя
new_item = All_(
    user_name="user_name",
    user_host=12,
    item_id=12,
    price=12,
    title="title",
    url="url"
)
try:
    session.commit()
except Exception as e:
    session.rollback()  # Откатить изменения в случае ошибки
    print(f"Error occurred: {e}")
finally:
    session.close()  # Закрыть сессию после завершения
