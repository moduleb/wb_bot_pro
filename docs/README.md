![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Aiogram](https://img.shields.io/badge/Aiogram-white?style=for-the-badge&logo=chatbot&color=%234796EC)
![Fastapi](https://img.shields.io/badge/Fastapi-black?style=for-the-badge&logo=fastapi&logoColor=white&color=%23009688)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-black?style=for-the-badge&logo=sqlalchemy&logoColor=red)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

Содержание:
- [Возможности](#features)  
- [Компоненты](#services)  
- [Установка и запуск](#install)  
- [Эндпоинты:](#endpoints)
  - [create](#create)
  - [get_all](#get_all)
  - [delete](#delete)

---

<a id="features"></a>
## Возможности:
- Добавление товара для отслеживания с помощью запроса к API или через бота
- Просмотр всех отслеживаемых товаров с помощью запроса к API или через бота
- Удаление товара из списка отслеживаемых с помощью запроса к API или через бота
- Получение уведомлений при изменении цены товара. Только в боте.

<a id="services"></a>
## Компоненты:
- Веб-приложение на FastAPI  
- Веб-сервер Nginx  
- База данных Postgres  
- Телеграм-бот на Aiogram 3  
- Очередь задач Redis
- Сервер выполнения задач Celery
- gRPC сервер для парсинга
- Админ панель на Django

<a id="install"></a>
## Установка и запуск:
>Для запуска вам потребуется [установить Docker](https://www.docker.com/).
1. Клонировать проект с Github:
```bash
  git clone https://github.com/moduleb/wb_bot_pro.git
```

2. Перейти в папку проекта:
```bash
  cd wb_bot_pro
```

3. Изменить файл RENAME.env, вписать токен от телеграм бота и другие переменные, переименовать файлн:
```bash
nano RENAME.env
```

4. Применить миграции
```shell
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

4. Собрать и запустить приложение в Docker:
```bash
sudo docker compose up -d --build
```

5. Остановить приложение:
```bash
sudo docker compose down
```

---
<a id="endpoints"></a>
## Эндпоинты:

Приложение доступно по адресу:
- на локальной машине http://localhost/
- на удаленном сервере http://<IP адрес сервера>
- .../docs - документация Swagger

<a id="create"></a>
### **[post]** .../api/v1/items

Принимает JSON с данными нового товара:
```json
{
  "url": "string", # ссылка на товар
  "user_id": "string" # id пользователя в телеграм
}
```

Возвращает 201 CREATED

---

<a id="get_all"></a>
### **[get]** .../api/v1/items
Параметры:
 - user_id: integer

Возвращает все добавленные товары для заданного пользователя:
```json
[
    {
        "id": 8,
        "user_id": 5312665858,
        "item_id": 176656692,
        "price": 1753,
        "title": "Педали для велосипеда на трех промышленных подшипниках",
        "url": "https://www.wildberries.ru/catalog/176656692/detail.aspx"
    },
    {
        "id": 9,
        "user_id": 5312665858,
        "item_id": 165835462,
        "price": 1338,
        "title": "Багажник на велосипед",
        "url": "https://www.wildberries.ru/catalog/165835462/detail.aspx"
    }
]
```

---

<a id="delete"></a>
### **[delete]** .../api/v1/items
Параметры:
 - user_id: integer
 - item_id: integer

Возвращает 204 NO CONTENT



