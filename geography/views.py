from .models import AreaSalaryAll, AreaCountAll, AreaSalaryProf, AreaCountProf
from django.shortcuts import render


def geography(request):
    area_salary_all = AreaSalaryAll.objects.values('area_name', 'average_salary')
    area_count_all = AreaCountAll.objects.values('area_name', 'vacancy_count')
    area_salary_prof = AreaSalaryProf.objects.values('area_name', 'average_salary')
    area_count_prof = AreaCountProf.objects.values('area_name', 'vacancy_count')

    context = {
        'area_salary_all': area_salary_all,
        'area_count_all': area_count_all,
        'area_salary_prof': area_salary_prof,
        'area_count_prof': area_count_prof,
        'prof': 'C/C++ программист',
    }
    return render(request, 'pages/geography.html', context)