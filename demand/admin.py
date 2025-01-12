# demand/admin.py
from django.contrib import admin
from .models import Vacancy

class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'region', 'salary_from', 'salary_to', 'salary_currency', 'publication_date')
    search_fields = ('title', 'company', 'skills')
    list_filter = ('region', 'salary_currency')
    ordering = ('-publication_date',)
    actions = ['make_published']

    def make_published(self, request, queryset):
        queryset.update(status='published')  # Пример действия для массового обновления
    make_published.short_description = 'Mark selected vacancies as published'

admin.site.register(Vacancy, VacancyAdmin)
