from django.shortcuts import render
from .models import Demand

def demand(request):
    # Попытка найти первую запись в модели Demand
    stat = Demand.objects.first()

    # Если запись не найдена
    if stat is None:
        return render(request, 'pages/demand.html', {'error': 'No data available'})

    context = {
        'salary_by_year_plot': stat.salary_by_year_plot if stat.salary_by_year_plot else None,
        'salary_by_year_table': stat.salary_by_year_table if stat.salary_by_year_table else None,
        'vacancy_by_year_plot': stat.vacancy_by_year_plot.url if stat.vacancy_by_year_plot else None,
        'vacancy_by_year_table': stat.vacancy_by_year_table if stat.vacancy_by_year_table else None,
        'prof': 'C/C++ программист',
    }

    return render(request, 'pages/demand.html', context)
