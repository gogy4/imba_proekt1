import requests
import re
from django.shortcuts import render

def clear_html(line: str) -> str:
    return re.sub(r'<.*?>', '', line.strip())

def get_hh_vacancies(profession):
    search_keywords = ['c++', 'с++']
    search_query = ' OR '.join(search_keywords)

    url = f'https://api.hh.ru/vacancies'
    params = {
        'text': search_query,
        'period': 1,
        'per_page': 10,
        'search_field': 'name',
        'order_by': 'publication_time',
    }
    headers = {'User-Agent': 'imbaproject/1.0 (younggogy@gmail.com)'}
    vacancies = []
    page = 0
    while True:
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        for item in data.get('items', []):
            try:
                vacancy_id = item.get('id', '')
                vacancy_url = f'https://api.hh.ru/vacancies/{vacancy_id}'
                vacancy_response = requests.get(vacancy_url, headers=headers)
                vacancy_data = vacancy_response.json()

                skills_list = vacancy_data.get('key_skills', [])
                skills = ', '.join(skill.get('name', '') for skill in skills_list)

                salary_info = vacancy_data.get('salary', {})
                salary_from = salary_info.get('from') if salary_info else None
                salary_to = salary_info.get('to') if salary_info else None
                salary_currency = salary_info.get('currency') if salary_info else None

                vacancies.append({
                    'title': vacancy_data.get('name', ''),
                    'description': clear_html(vacancy_data.get('description', '')),
                    'skills': skills,
                    'company': vacancy_data.get('employer', {}).get('name', ''),
                    'salary_from': salary_from,
                    'salary_to': salary_to,
                    'salary_currency': salary_currency,
                    'region': vacancy_data.get('area', {}).get('name', ''),
                    'publication_date': item.get('published_at', '')
                })

            except Exception as e:
                print(f"Error processing vacancy {item.get('id', '')}: {e}")

        if not data.get('items'):
            break

        if len(vacancies) >= 10:
            break

        page += 1

    return vacancies

def last_vacancies(request):
    profession = 'Game Developer'
    vacancies = get_hh_vacancies(profession)

    context = {'vacancies': vacancies, 'profession': profession}
    return render(request, 'pages/last_vacancies.html', context)