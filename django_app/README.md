django-admin startproject django_app
cd django_app

> settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',  # или IP-адрес вашего PostgreSQL
        'PORT': '5432',       # или другой порт, если он изменен
    }
}

python manage.py migrate
python manage.py startapp wb_bot_admin

> settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wb_bot_admin'
]

python manage.py migrate --fake-initial
python manage.py inspectdb > wb_bot_admin/models.py
python manage.py makemigrations wb_bot_admin
python manage.py migrate --fake wb_bot_admin

> admin.py
from django.contrib import admin
from .models import All
@admin.register(All)
class AllAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'item_id', 'price', 'title', 'url')  # Укажите поля, которые хотите отображать в админке

python manage.py runserver

> settings.py
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'localhost', '127.0.0.1']
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

python manage.py collectstatic

## Для разработки
> urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
]
if settings.DEBUG:  # Убедитесь, что это только для разработки
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

