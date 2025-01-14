from django.shortcuts import render
from .models import Skills

def skills(request):
    # Попытка найти первую запись в базе данных
    stat = Skills.objects.first()

    # Если запись не найдена
    if stat is None:
        return render(request, 'pages/statistics_page.html', {'error': 'Нет данных'})

    # Перечень доступных лет
    year = list(range(2015, 2025))
    # Получаем год из запроса, по умолчанию текущий год
    current_year = request.GET.get('year', str(year[-1]))

    # Динамическая загрузка данных для текущего года
    top_skills_plot = getattr(stat, f"top_skills_plot_{current_year}", None)
    top_skills_table = getattr(stat, f"top_skills_table_{current_year}", None)

    # Проверка на None для top_skills_plot
    top_skills_plot_url = top_skills_plot.url if top_skills_plot else None

    # Формируем контекст для рендеринга шаблона
    context = {
        'top_skills_plot': top_skills_plot_url,  # График топ-умений
        'top_skills_table': top_skills_table,  # Таблица топ-умений
        'unique_years': year,  # Список доступных лет
        'selected_year': current_year,  # Выбранный год
    }

    # Рендерим страницу с данными
    return render(request, 'pages/skills.html', context)
