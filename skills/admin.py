from django.contrib import admin
from .models import Skills
# Регистрируем модель с кастомными настройками в админке
admin.site.register(Skills)
