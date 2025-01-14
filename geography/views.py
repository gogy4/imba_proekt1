from .models import AreaSalaryAll, AreaCountAll, AreaSalaryProf, AreaCountProf, Geography
from django.shortcuts import render


def geography(request):
    # Получение данных из моделей
    area_salary_all = AreaSalaryAll.objects.values('area_name', 'average_salary')
    area_count_all = AreaCountAll.objects.values('area_name', 'vacancy_count')
    area_salary_prof = AreaSalaryProf.objects.values('area_name', 'average_salary')
    area_count_prof = AreaCountProf.objects.values('area_name', 'vacancy_count')

    # Попытка найти первую запись в модели Geography
    stat = Geography.objects.first()

    # Если запись не найдена
    if stat is None:
        return render(request, 'pages/geography.html', {'error': 'No data available'})

    # Формируем контекст
    context = {
        'salary_by_city_plot': stat.salary_by_city_plot.url if stat.salary_by_city_plot else None,
        'salary_by_city_table': stat.salary_by_city_table if stat.salary_by_city_table else None,
        'vacancy_by_city_plot': stat.vacancy_by_city_plot.url if stat.vacancy_by_city_plot else None,
        'vacancy_by_city_table': stat.vacancy_by_city_table if stat.vacancy_by_city_table else None,
        'area_salary_all': area_salary_all,
        'area_count_all': area_count_all,
        'area_salary_prof': area_salary_prof,
        'area_count_prof': area_count_prof,
        'prof': 'C/C++ программист',
    }

    return render(request, 'pages/geography.html', context)
