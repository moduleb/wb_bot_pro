[//]: # Запуск POSTGRESQL
docker run --name postgres-container -e POSTGRES_USER=user -e POSTGRES_PASSWORD=passw53 -e POSTGRES_DB=db53 -p 5432:5432 -d postgres

pip install asyncpg alembic sqlalchemy
pip3 install psycopg2-binary

# Инициализируем Alembic
alembic init migrations

# Изменения в файлах
[alembic.ini]
sqlalchemy.url = postgresql://username:password@localhost/dbname

# получить ip контейнера
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres  

[migrations/.env]
from models import Base
target_metadata = Base.metadata
---------------------

# Создаем миграцию
alembic revision --autogenerate -m "Initial migration"

# Применяем миграцию
alembic upgrade head

---

# Проверка баз в докере
docker exec -it 3ba7fe48f421 bash
ls - список команд
psql -U user -d db53

или сразу 
docker exec -it 3ba7fe48f421 psql -U user -d db53

### Основные команды PostgreSQL

1. **Показать базы данных**:
   Чтобы отобразить все базы данных, используйте команду:

   ```sql
   \l
   ```

2. **Подключение к базе данных**:
   Если вы хотите подключиться к конкретной базе данных, используйте:

   ```sql
   \c имя_базы_данных
   ```

3. **Показать таблицы**:
   Чтобы отобразить все таблицы в текущей базе данных, используйте:

   ```sql
   \dt
   ```

4. **Показать структуру таблицы**:
   Чтобы увидеть структуру конкретной таблицы, используйте:

   ```sql
   \d имя_таблицы
   ```

5. **Выполнение SQL-запросов**:
   Чтобы выполнить SQL-запрос, например, выбрать все записи из таблицы, используйте:

   ```sql
   SELECT * FROM имя_таблицы;
   ```
   
# Создать другую базу данных 
CREATE DATABASE new_database;
\l проверка
\с new_database  подключиться
   
# Вывести количество записей в таблице
SELECT COUNT(*) FROM mytable_;

# Убедиться что я в нужной база
SELECT current_database();

