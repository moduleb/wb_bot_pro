from django.contrib import admin
from .models import All

@admin.register(All)
class AllAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'item_id', 'price', 'title', 'url')  # Укажите поля, которые хотите отображать в админке
