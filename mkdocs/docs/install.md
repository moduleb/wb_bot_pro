
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

## Настроить переменные окружения
Изменить файл RENAME.env, вписать токен от телеграм бота и другие переменные если необходимо, сохранить:
```bash
nano RENAME.env
```

Переименовать файл RENAME.env -> .env
```sh
mv RENAME.env .env
```

## Запустить
```bash
sudo docker compose up -d --build
```

## Применить миграции
```shell
docker exec -it -w /app/db fastapi alembic upgrade head &&
docker exec -it django python3 manage.py migrate
```

## Создать пользователя для админки Django
```sh
docker exec -it django python3 manage.py createsuperuser
```

## Проверить
Теперь можно отправлять сообщения боту, токен которого вы указали в файле .env  
или отправлять запросы к API по адресу:  
- на локальной машине `http://localhost/`  
- на удаленном сервере `http://<IP адрес сервера>`  
- `/docs` - документация Swagger  
- `/admin` - админ панель Django (логин и пароль, который ввели при создании суперпользователя)

## Остановить:
```bash
sudo docker compose down
```