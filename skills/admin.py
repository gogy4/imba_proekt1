from django.contrib import admin
from .models import Skills


class SkillsAdmin(admin.ModelAdmin):
    list_display = [f'top_skills_plot_{year}' for year in range(2015, 2025)]
    search_fields = [f'top_skills_plot_{year}' for year in range(2015, 2025)]

admin.site.register(Skills, SkillsAdmin)