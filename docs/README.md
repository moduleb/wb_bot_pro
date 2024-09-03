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

--- проект в разработке ---
------

## Бот для Телеграм, отслеживающий изменение цены на Wildberries.

Что умеет бот:
  + принимает ссылку на товар и присылает уведомление при изменении цены.
  + позволяет добавлять несколько товаров для отслеживания.

Проект включает:
Тг бот на вебхуках
Fastapi-swagger-websockets
Postgre-sqlalchemy-alembic-redis для хранения данных
Celery-redis для задач
Интеграция с вайдбеоис апи
Docker-compose для развертывания
Github-flow
Nginx-ssl
Все это на двух серверах с локальной сетью
nginx(80,443 +postgre+  бот + джанго(80)
Еще джанго админка
Управление серверов ansible
Развериывание контейнеров  docker swarm

Из админки
1. узнать статус бота (вкл или выключен)
2. Запустить, остановить, перезагрузить бота
3. Назначить админов бота
4. Редактировать данные пользователей
5. Блокировать пользователей
6. Смотреть статистику бота в виде графиков и столбцов
