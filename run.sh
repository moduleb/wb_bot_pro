#!/bin/bash

# Функция для проверки, запущен ли Docker
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "Docker не запущен. Пожалуйста, запустите Docker."
        exit 1
    fi
}

# Проверка операционной системы
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Для Linux
    if ! systemctl is-active --quiet docker; then
        echo "Запуск демона Docker..."
        sudo systemctl start docker
    fi
    check_docker

elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Для macOS
    check_docker

else
    echo "Неизвестная операционная система: $OSTYPE"
    exit 1
fi

# Загрузка переменных окружения из файла .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Файл .env не найден!"
    exit 1
fi

# Проверка, запущен ли контейнер PostgreSQL
#if [ "$(docker ps -q -f name=$POSTGRES_CONTAINER_NAME)" ]; then
#    echo "Контейнер PostgreSQL уже запущен."
#else
#    echo "Запуск контейнера PostgreSQL..."
#    docker run --name $POSTGRES_CONTAINER_NAME -e POSTGRES_USER=$POSTGRES_USER -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -e POSTGRES_DB=$POSTGRES_DB_NAME -d postgres
#fi

# Проверка доступности базы данных с помощью pg_isready внутри контейнера
echo "Проверка доступности базы данных PostgreSQL..."
for i in {1..10}; do
    if docker exec postgres pg_isready -U $POSTGRES_USER -d $POSTGRES_DB_NAME; then
        echo "База данных PostgreSQL доступна."
        break
    else
        echo "База данных PostgreSQL недоступна."
        echo "Запуск контейнера PostgreSQL..."
        docker run --name postgres -e POSTGRES_USER=$POSTGRES_USER -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -e POSTGRES_DB=$POSTGRES_DB_NAME -d postgres
        sleep 1
    fi
done

# Проверка доступности базы данных с помощью pg_isready внутри контейнера
echo "Проверка доступности Redis..."
for i in {1..10}; do
    if docker exec redis redis-cli ping | grep -q PONG; then
        echo "Redis доступен."
        break
    else
        echo "Redis недоступен."
        echo "Запуск контейнера Redis..."
        docker run --name redis -d -p 6379:6379 redis
        sleep 1
    fi
done

# Запуск Celery
#celery -A celery_app.celery_config worker --beat --loglevel=info &

# Запускаем бота
echo "Запуск бота..."
python3 bot_app/run.py
