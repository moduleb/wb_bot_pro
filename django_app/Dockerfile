# Используем официальный образ Python
#FROM python:3.12-slim
FROM python:3.12-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Выполняем миграции (по желанию, можно сделать в docker-compose)
#RUN python manage.py migrate

# Открываем порт, на котором будет работать Django
#EXPOSE 8000

# Команда для запуска сервера
#CMD ["gunicorn", "django_app.wsgi:application", "--bind", "0.0.0.0:8000"]