from django.shortcuts import render
from .models import StatisticsPage

def statistics_page(request):
    # Попытка найти первую запись в базе данных
    stat = StatisticsPage.objects.first()

    # Если запись не найдена
    if stat is None:
        return render(request, 'pages/statistics_page.html', {'error': 'No data available'})

    year = list(range(2015, 2025))  # Перечень доступных лет
    current_year = request.GET.get('year', str(year[-1]))  # Получаем год из запроса, по умолчанию текущий год

    # Динамическая загрузка данных для текущего года
    top_skills_plot = getattr(stat, f"top_skills_plot_{current_year}", None)
    top_skills_table = getattr(stat, f"top_skills_table_{current_year}", None)

    # Получаем URL для изображений, если они существуют
    top_skills_plot_url = top_skills_plot.url if top_skills_plot else None
    salary_by_year_plot_url = stat.salary_by_year_plot.url if stat.salary_by_year_plot else None
    vacancies_by_year_plot_url = stat.vacancies_by_year_plot.url if stat.vacancies_by_year_plot else None
    salary_by_city_plot_url = stat.salary_by_city_plot.url if stat.salary_by_city_plot else None
    vacancy_share_by_city_plot_url = stat.vacancy_share_by_city_plot.url if stat.vacancy_share_by_city_plot else None

    context = {
        'top_skills_plot': top_skills_plot_url,
        'top_skills_table': top_skills_table,
        'unique_years': year,  # Список всех доступных лет
        'selected_year': current_year,  # Текущий выбранный год
        'salary_by_year_plot': salary_by_year_plot_url,
        'salary_by_year_table': stat.salary_by_year_table,
        'vacancies_by_year_plot': vacancies_by_year_plot_url,
        'vacancies_by_year_table': stat.vacancies_by_year_table,
        'salary_by_city_plot': salary_by_city_plot_url,
        'salary_by_city_table': stat.salary_by_city_table,
        'vacancy_share_by_city_plot': vacancy_share_by_city_plot_url,
        'vacancy_share_by_city_table': stat.vacancy_share_by_city_table,
    }

    return render(request, 'pages/statistics_page.html', context)
