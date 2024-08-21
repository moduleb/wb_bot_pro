![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Aiogram](https://img.shields.io/badge/Aiogram-white?style=for-the-badge&logo=chatbot&color=%234796EC)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

--- проект в разработке ---
------

## Бот для Телеграм, отслеживающий изменение цены на Wildberries.

Что умеет бот:
  + принимает ссылку на товар и присылает уведомление при изменении цены.
  + позволяет добавлять несколько товаров для отслеживания.

Проект включает 
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
