from django.shortcuts import render
from .models import StatisticsPage

def statistics_page(request):
    # Попытка найти первую запись в базе данных
    stat = StatisticsPage.objects.first()

    # Если запись не найдена
    if stat is None:
        return render(request, 'pages/statistics_page.html', {'error': 'No data available'})

    year = list(range(2015, 2025))
    current_year = request.GET.get('year', str(year[-1]))

    top_skills_chart = getattr(stat, f"top_skills_graph_{current_year}", None)
    top_skills_table = getattr(stat, f"top_skill_table_{current_year}", None)

    # Пример проверки на None
    top_skills_chart_url = top_skills_chart.url if top_skills_chart else None
    salary_by_year_plot_url = stat.salary_by_year_plot.url if stat.salary_by_year_plot else None
    vacancies_by_year_plot_url = stat.vacancies_by_year_plot.url if stat.vacancies_by_year_plot else None
    salary_by_city_plot_url = stat.salary_by_city_plot.url if stat.salary_by_city_plot else None
    vacancy_share_by_city_plot_url = stat.vacancy_share_by_city_plot.url if stat.vacancy_share_by_city_plot else None

    context = {
        'top_skills_chart': top_skills_chart_url,
        'top_skills_table': top_skills_table,
        'unique_years': year,
        'selected_year': current_year,
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
