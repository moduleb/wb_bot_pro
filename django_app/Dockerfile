# Используем официальный образ Python
FROM python:3.12-slim

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
EXPOSE 8000

# Команда для запуска сервера
#CMD ["python", "manage.py", "runserver"]