FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install -r requirements.txt --no-cache-dir

# Удаляем символическую ссылку (если она есть)
#RUN rm -rf shared

# Копируем оригинальную папку вместо символической ссылки
#COPY ../shared /app/shared

# Копируем остальные файлы проекта в контейнер
COPY . .

# Запуск приложения
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]
