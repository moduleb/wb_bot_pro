from celery import Celery

import config

# Создаем экземпляр Celery
app = Celery('main', broker=config.REDIS_CONNECTION_STRING,
             backend=config.REDIS_CONNECTION_STRING)

# Установите параметр для повторных попыток подключения
app.conf.broker_connection_retry_on_startup = True

# Импортируйте модуль с задачами НЕ УБИРАТЬ!!! import tasks.task1

# Настройки Celery Beat
app.conf.beat_schedule = {
    'test_task': {
        'task': 'celery_app.tasks.task1.notify_price_changes', # имя задачи
        'schedule': 10.0,  # Запускать каждые 5 секунды
        # 'args': (bot),
    },
}
