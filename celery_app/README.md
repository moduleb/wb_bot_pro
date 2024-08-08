
celery -A celery_app.celery_config worker --beat --loglevel=debug


```bash
pip install celery redis flower
docker run --name redis -d -p 6379:6379 redis
celery -A celery_config worker --beat --loglevel=info
celery -A tasks flower
```