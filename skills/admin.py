from django.contrib import admin
from .models import Skills


# Настройка отображения и поиска для модели Skills в админке
class SkillsAdmin(admin.ModelAdmin):
    # Отображаем графики топ-20 навыков для каждого года с 2015 по 2024
    list_display = [f'top_skills_plot_{year}' for year in range(2015, 2025)]

    # Настройка полей для поиска в админке
    search_fields = [f'top_skills_plot_{year}' for year in range(2015, 2025)]


# Регистрируем модель с кастомными настройками в админке
admin.site.register(Skills, SkillsAdmin)
