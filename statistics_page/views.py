import requests
import re
import pandas as pd
import matplotlib.pyplot as plt
import os
from django.shortcuts import render
from .models import Vacancy
from django.db.models import Count, Avg, F, FloatField
from django.db.models.functions import ExtractYear

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
        'search_field': 'name',
        'only_with_salary': 'true',
        'order_by': 'publication_time',
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

# Вспомогательная функция для конвертации валюты
def convert_salary(salary, currency, date):
    if not salary or not currency or currency == 'RUR':
        return salary

    currency_df = pd.read_csv('data/currency.csv')
    rate = currency_df[(currency_df['date'] == date) & (currency_df['currency'] == currency)]['rate'].values
    return salary * rate[0] if len(rate) > 0 else salary

# Статистика

def statistics_page(request):
    vacancies = Vacancy.objects.all()

    # Динамика зарплат по годам
    salary_dynamic = vacancies.annotate(year=ExtractYear('publication_date'))\
        .exclude(salary_from__gt=10000000)\
        .values('year')\
        .annotate(avg_salary=Avg(F('salary_from') + F('salary_to') / 2, output_field=FloatField()))\
        .order_by('year')

    # Динамика количества вакансий по годам
    vacancy_dynamic = vacancies.annotate(year=ExtractYear('publication_date'))\
        .values('year')\
        .annotate(count=Count('id'))\
        .order_by('year')

    # Уровень зарплат по городам
    city_salary = vacancies.exclude(salary_from__gt=10000000)\
        .values('region')\
        .annotate(avg_salary=Avg(F('salary_from') + F('salary_to') / 2, output_field=FloatField()))\
        .order_by('-avg_salary')

    # Доля вакансий по городам
    city_vacancies = vacancies.values('region')\
        .annotate(count=Count('id'))\
        .order_by('-count')

    # ТОП-20 навыков
    skills = pd.DataFrame(Vacancy.objects.values_list('skills', flat=True))
    try:
        skills = skills[0].str.split(', ').explode().value_counts().head(20)
    except KeyError:
        skills = pd.Series(dtype='int')

    # Визуализация
    os.makedirs('static_dev/statics_page/img/', exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.bar(salary_dynamic.values_list('year', flat=True), salary_dynamic.values_list('avg_salary', flat=True))
    plt.title('Динамика уровня зарплат по годам')
    plt.savefig('static_dev/statics_page/img/salary_dynamic.png')

    plt.figure(figsize=(10, 6))
    plt.bar(vacancy_dynamic.values_list('year', flat=True), vacancy_dynamic.values_list('count', flat=True))
    plt.title('Динамика количества вакансий по годам')
    plt.savefig('static_dev/statics_page/img/vacancy_dynamic.png')

    plt.figure(figsize=(10, 6))
    plt.bar(city_salary.values_list('region', flat=True), city_salary.values_list('avg_salary', flat=True))
    plt.xticks(rotation=45)
    plt.title('Уровень зарплат по городам')
    plt.savefig('static_dev/statics_page/img/city_salary.png')

    context = {
        'salary_dynamic': salary_dynamic,
        'vacancy_dynamic': vacancy_dynamic,
        'city_salary': city_salary,
        'city_vacancies': city_vacancies,
        'skills': skills,
    }

    return render(request, 'pages/statistics_page.html', context)
