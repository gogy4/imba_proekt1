from django.contrib import admin
from .models import StatisticsPage


# Регистрируем модель StatisticsPage в админке с настройками из StatisticsPageAdmin
admin.site.register(StatisticsPage)
