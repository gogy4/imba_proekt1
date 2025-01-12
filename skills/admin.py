# skills/admin.py
from django.contrib import admin
from .models import TopSkillsAll, TopSkillsProf

class TopSkillsAllAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'count', 'year')
    search_fields = ('skill_name',)

class TopSkillsProfAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'count', 'year')
    search_fields = ('skill_name',)

admin.site.register(TopSkillsAll, TopSkillsAllAdmin)
admin.site.register(TopSkillsProf, TopSkillsProfAdmin)
