# geography/admin.py
from django.contrib import admin
from .models import AreaSalaryAll, AreaCountAll, AreaSalaryProf, AreaCountProf

class AreaSalaryAllAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'average_salary')
    search_fields = ('area_name',)

class AreaCountAllAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'vacancy_count')
    search_fields = ('area_name',)

class AreaSalaryProfAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'average_salary')
    search_fields = ('area_name',)

class AreaCountProfAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'vacancy_count')
    search_fields = ('area_name',)

admin.site.register(AreaSalaryAll, AreaSalaryAllAdmin)
admin.site.register(AreaCountAll, AreaCountAllAdmin)
admin.site.register(AreaSalaryProf, AreaSalaryProfAdmin)
admin.site.register(AreaCountProf, AreaCountProfAdmin)
