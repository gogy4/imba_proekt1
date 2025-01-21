from django.contrib import admin
from .models import Home
# Регистрируем модель с кастомными настройками в админке
admin.site.register(Home)
