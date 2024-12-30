from django.shortcuts import render
from .models import DynamicSalaryAll, DynamicCountAll, DynamicSalaryProf, DynamicCountProf, AreaSalaryAll, AreaCountAll, AreaSalaryProf, AreaCountProf
from .models import Vacancy
import requests
import re


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
        'prof': 'C/C++ программист',
    }
    return render(request, 'pages/demand.html', context)

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

def skills(request):
    return render(request, 'base.html')

def clear_html(line: str) -> str:
    return re.sub(r'<.*?>', '', line.strip())


def get_hh_vacancies(profession):
    url = f'https://api.hh.ru/vacancies?text={profession}&period=1&per_page=10'
    headers = {'User-Agent': 'imbaproject/1.0 (younggogy@gmail.com)'}

    response = requests.get(url, headers=headers)
    data = response.json()

    vacancies = []
    for item in data.get('items', []):
        vacancy_id = item.get('id', '')
        url = f'https://api.hh.ru/vacancies/{vacancy_id}'
        headers = {'User-Agent': 'imbaproject/1.0 (younggogy@gmail.com)'}
        response = requests.get(url, headers=headers)
        vacancy_data = response.json()

        skills_list = vacancy_data.get('key_skills', [])
        skills = ', '.join(skill.get('name', '') for skill in skills_list)

        salary_info = vacancy_data.get('salary', {})
        vacancy = {
            'title': vacancy_data.get('name', ''),
            'description': clear_html(vacancy_data.get('description', '')),
            'skills': skills,
            'company': vacancy_data.get('employer', {}).get('name', ''),
            'salary_from': salary_info.get('from', None) if salary_info else None,
            'salary_to': salary_info.get('to', None) if salary_info else None,
            'salary_currency': salary_info.get('currency', None) if salary_info else None,
            'region': vacancy_data.get('area', {}).get('name', ''),
            'publication_date': item.get('published_at', '')
        }
        vacancies.append(vacancy)

    return vacancies


def last_vacancies(request):
    profession = 'C/C++'
    vacancies = get_hh_vacancies(profession)
    for vacancy_data in vacancies:
        Vacancy.objects.create(**vacancy_data)

    context = {'vacancies': vacancies, 'profession': profession}
    return render(request, 'latest_vacancies.html', context)