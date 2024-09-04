
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

3. Изменить файл RENAME.env, вписать токен от телеграм бота и другие переменные если необходимо, сохранить:
```bash
nano RENAME.env
```

4. переименовать файл RENAME.env -> .env
```sh
mv RENAME.env .env
```

5. Собрать и запустить приложение в Docker:
```bash
sudo docker compose up -d --build
```

6. Применить миграции
```shell
docker exec -it -w /app/db fastapi alembic upgrade head &&
docker exec -it django python3 manage.py migrate
```

7. Создать пользователя для админки Django
```sh
docker exec -it django python3 manage.py createsuperuser
```
`
8. Остановить приложение:
```bash
sudo docker compose down
```

Теперь можно отправлять сообщения боту, токен которого вы указали в файле .env
Приложение доступно по адресу:  
- на локальной машине `http://localhost/`  
- на удаленном сервере `http://<IP адрес сервера>`  
- `/docs` - документация Swagger  
- `/admin` - админ панель Django (логин и пароль, который ввели при создании суперпользователя)