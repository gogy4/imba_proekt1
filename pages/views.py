from django.shortcuts import render
from .models import DynamicSalaryAll, DynamicCountAll, DynamicSalaryProf, DynamicCountProf


def home(request):
    return render(request, 'pages/home.html')

def statistics(request):
    return render(request, 'base.html')

def demand(request):
    dynamic_salary_all = DynamicSalaryAll.objects.values('year', 'average_salary')
    dynamic_count_all = DynamicCountAll.objects.values('year', 'vacancy_count')
    dynamic_salary_prof = DynamicSalaryProf.objects.values('year', 'average_salary')
    dynamic_count_prof = DynamicCountProf.objects.values('year', 'vacancy_count')
    context = {
        'dynamic_salary_all': dynamic_salary_all,
        'dynamic_count_all': dynamic_count_all,
        'dynamic_salary_prof': dynamic_salary_prof,
        'dynamic_count_prof': dynamic_count_prof,
        'prof': 'C++ Разработчик',
    }
    return render(request, 'pages/demand.html', context)

def geography(request):
    return render(request, 'base.html')

def skills(request):
    return render(request, 'base.html')

def last_vacancies(request):
    return render(request, 'base.html')