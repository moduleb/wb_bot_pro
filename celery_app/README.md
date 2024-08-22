
celery -A celery_app.celery_config worker --beat --loglevel=debug


```bash
pip install celery redis flower
docker run --name redis -d -p 6379:6379 redis
celery -A celery_app.run worker --beat --loglevel=info
celery -A tasks flower
```

#
# # Отправляем задачу в очередь
# result = square.delay()
#
# # Получаем результат
# print('Задача отправлена, ожидаем результат...')
# print('Результат:', result.get(timeout=10))  # Получаем результат с таймаутом