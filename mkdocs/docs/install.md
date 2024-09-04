
Для запуска вам потребуется [установить Docker](https://www.docker.com/).  
#
## Скачать проект
Клонировать проект с Github:
```bash
  git clone https://github.com/moduleb/wb_bot_pro.git
```

Перейти в папку проекта:
```bash
  cd wb_bot_pro
```

## Настроить приложение
Изменить файл RENAME.env, вписать токен от телеграм бота и другие переменные, переименовать файл:
```bash
nano RENAME.env
```

Применить миграции
```shell
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Запустить
Собрать и запустить приложение в Docker:
```bash
sudo docker compose up -d --build
```

Остановить приложение:
```bash
sudo docker compose down
```

