import requests
import re
from django.shortcuts import render

# Очистка HTML-тегов из описания
def clear_html(line: str) -> str:
    return re.sub(r'<.*?>', '', line.strip())

# Получение вакансий с HH.ru

def get_hh_vacancies(profession):
    url = f'https://api.hh.ru/vacancies'
    params = {
        'text': profession,
        'period': 3,  # Ищем за последние 3 дня
        'per_page': 10,  # Количество результатов на странице
        'search_field': 'name',  # Поиск в названии и описании
        'order_by': 'publication_time',  # Сортировка по времени публикации
    }
    headers = {'User-Agent': 'imbaproject/1.0 (younggogy@gmail.com)'}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    vacancies = []
    for item in data.get('items', []):
        try:
            vacancy_id = item.get('id', '')
            vacancy_url = f'https://api.hh.ru/vacancies/{vacancy_id}'
            vacancy_response = requests.get(vacancy_url, headers=headers)
            vacancy_data = vacancy_response.json()
            # Проверка на наличие данных о навыках
            skills_list = vacancy_data.get('key_skills', [])
            skills = ', '.join(skill.get('name', '') for skill in skills_list)

            # Проверка на наличие данных о зарплате
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

    return vacancies



# View-функция для отображения последних вакансий

def last_vacancies(request):
    profession = 'C/C++ программист'
    vacancies = get_hh_vacancies(profession)
    context = {'vacancies': vacancies, 'profession': profession}
    return render(request, 'pages/last_vacancies.html', context)
