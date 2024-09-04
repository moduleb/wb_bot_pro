
Для запуска вам потребуется [установить Docker](https://www.docker.com/).  
#
## Скачать проект
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

4. Собрать и запустить приложение в Docker:
```bash
sudo docker compose up -d --build
```

5. Применить миграции
```shell
docker exec -it -w /app/db fastapi alembic upgrade head &&
docker exec -it django python3 manage.py migrate
```

6. Создать пользователя для админки Django
```sh
docker exec -it django python3 manage.py createsuoeruser
```
`
7. Остановить приложение:
```bash
sudo docker compose down
```

