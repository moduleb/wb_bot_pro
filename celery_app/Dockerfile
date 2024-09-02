#FROM python:3.12-slim
FROM python:3.12-alpine
RUN #apk add --no-cache gcc musl-dev

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install -r requirements.txt --no-cache-dir

# Копируем остальные файлы проекта в контейнер
COPY . .
#COPY . ./grpc_app
#COPY ./celery_app ./celery_app

# Устанавливаем рабочую директорию для запуска приложения
#WORKDIR /app/grpc_app

# Запуск приложения
#CMD ["python", "run.py"]
CMD ["celery", "-A", "run", "worker", "--beat", "--loglevel=info"]