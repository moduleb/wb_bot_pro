from celery import Celery



REDIS_CONNECTION_STRING = "redis://localhost:6379/0"

# Создаем экземпляр Celery
app = Celery('main', broker=REDIS_CONNECTION_STRING,
             backend=REDIS_CONNECTION_STRING)

# Установите параметр для повторных попыток подключения
app.conf.broker_connection_retry_on_startup = True

# Импортируйте модуль с задачами НЕ УБИРАТЬ!!! import tasks.task1
import celery_app.tasks.task1

# Настройки Celery Beat
app.conf.beat_schedule = {
    'test_task': {
        'task': 'celery_app.tasks.task1.notify_price_changes', # имя задачи
        'schedule': 3.0,  # Запускать каждые 3 секунды
        # 'args': (bot),
    },
}
