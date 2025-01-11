from django.shortcuts import render
from .models import TopSkillsAll, TopSkillsProf


def skills(request):
    unique_years = list(range(2017, 2024))
    selected_year = request.GET.get('year', unique_years[-1])  # По умолчанию выбран последний год

    skills_all = TopSkillsAll.objects.filter(year=selected_year)
    skills_prof = TopSkillsProf.objects.filter(year=selected_year)

    context = {
        'unique_years': unique_years,
        'selected_year': int(selected_year),
        'skills_all': skills_all,
        'skills_prof': skills_prof,
        'prof': 'C/C++ программист',
    }

    return render(request, 'pages/skills.html', context)