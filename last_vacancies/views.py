import requests
import re
from django.shortcuts import render
from .models import Vacancy

# Очистка HTML-тегов из описания
def clear_html(line: str) -> str:
    return re.sub(r'<.*?>', '', line.strip())

# Получение вакансий с HH.ru

def get_hh_vacancies(profession):
    url = f'https://api.hh.ru/vacancies'
    params = {
        'text': profession,
        'period': 1,
        'per_page': 10,
        'search_field': 'name',  # Искать только в названии вакансии
        'only_with_salary': 'true',  # Только с указанной зарплатой
        'order_by': 'publication_time',  # Сортировка по дате публикации
    }
    headers = {'User-Agent': 'imbaproject/1.0 (younggogy@gmail.com)'}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    vacancies = []
    for item in data.get('items', []):
        vacancy_id = item.get('id', '')
        vacancy_url = f'https://api.hh.ru/vacancies/{vacancy_id}'
        response = requests.get(vacancy_url, headers=headers)
        vacancy_data = response.json()

        skills_list = vacancy_data.get('key_skills', [])
        skills = ', '.join(skill.get('name', '') for skill in skills_list)

        salary_info = vacancy_data.get('salary', {})
        vacancy = {
            'title': vacancy_data.get('name', ''),
            'description': clear_html(vacancy_data.get('description', '')),
            'skills': skills,
            'company': vacancy_data.get('employer', {}).get('name', ''),
            'salary_from': salary_info.get('from', None),
            'salary_to': salary_info.get('to', None),
            'salary_currency': salary_info.get('currency', None),
            'region': vacancy_data.get('area', {}).get('name', ''),
            'publication_date': item.get('published_at', '')
        }
        vacancies.append(vacancy)

    return vacancies

# View-функция для отображения последних вакансий

def last_vacancies(request):
    profession = 'C/C++'
    vacancies = get_hh_vacancies(profession)
    Vacancy.objects.bulk_create([Vacancy(**vacancy_data) for vacancy_data in vacancies])

    context = {'vacancies': vacancies, 'profession': profession}
    return render(request, 'pages/last_vacancies.html', context)
