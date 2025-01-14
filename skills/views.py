from django.shortcuts import render
from .models import Skills

def skills(request):
    # Попытка найти первую запись в базе данных
    stat = Skills.objects.first()

    # Если запись не найдена
    if stat is None:
        return render(request, 'pages/skills.html', {'error': 'No data available'})

    year = list(range(2015, 2025))
    current_year = request.GET.get('year', str(year[-1]))

    # Получаем график и таблицу для выбранного года
    top_skills_plot = getattr(stat, f"top_skills_plot_{current_year}", None)
    top_skills_table = getattr(stat, f"top_skill_table_{current_year}", None)

    # Проверка на None для top_skills_chart
    top_skills_plot_url = top_skills_plot.url if top_skills_plot else None

    context = {
        'top_skills_plot': top_skills_plot_url,
        'top_skills_table': top_skills_table,
        'unique_years': year,
        'selected_year': current_year,
    }

    return render(request, 'pages/skills.html', context)
