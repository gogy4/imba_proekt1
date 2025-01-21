import requests
import re
from django.shortcuts import render

# Функция для удаления HTML-тегов из строки
def clear_html(line: str) -> str:
    return re.sub(r'<.*?>', '', line.strip())

# Функция для получения списка вакансий по определенной профессии с использованием API hh.ru
def get_hh_vacancies():
    # Ключевые слова для поиска
    search_keywords = ['c++', 'с++']
    # Создание поискового запроса с использованием логического оператора OR
    search_query = ' OR '.join(search_keywords)

    # URL для API hh.ru
    url = f'https://api.hh.ru/vacancies'
    # Параметры запроса
    params = {
        'text': search_query,  # Поиск по указанным ключевым словам
        'period': 1,  # Период в днях (1 день)
        'per_page': 10,  # Количество результатов на страницу
        'search_field': 'name',  # Поле для поиска (название вакансии)
        'order_by': 'publication_time',  # Сортировка по времени публикации
    }
    # Заголовки для HTTP-запроса
    headers = {'User-Agent': 'imbaproject/1.0 (younggogy@gmail.com)'}
    vacancies = []  # Список для сохранения информации о вакансиях
    page = 0  # Номер страницы

    # Цикл для получения данных с нескольких страниц
    while True:
        params['page'] = page  # Устанавливаем текущую страницу в параметры запроса
        response = requests.get(url, headers=headers, params=params)  # Отправляем запрос
        data = response.json()  # Парсим JSON-ответ

        # Обработка вакансий из текущей страницы
        for item in data.get('items', []):
            try:
                # Получаем ID вакансии и формируем URL для получения детальной информации
                vacancy_id = item.get('id', '')
                vacancy_url = f'https://api.hh.ru/vacancies/{vacancy_id}'
                vacancy_response = requests.get(vacancy_url, headers=headers)  # Запрашиваем данные вакансии
                vacancy_data = vacancy_response.json()  # Парсим JSON-ответ

                # Получение списка ключевых навыков
                skills_list = vacancy_data.get('key_skills', [])
                skills = ', '.join(skill.get('name', '') for skill in skills_list)

                # Получение информации о зарплате
                salary_info = vacancy_data.get('salary', {})
                salary_from = salary_info.get('from') if salary_info else None
                salary_to = salary_info.get('to') if salary_info else None
                salary_currency = salary_info.get('currency') if salary_info else None

                # Сохранение информации о вакансии в список
                vacancies.append({
                    'title': vacancy_data.get('name', ''),  # Название вакансии
                    'description': clear_html(vacancy_data.get('description', '')),  # Описание без HTML
                    'skills': skills,  # Ключевые навыки
                    'company': vacancy_data.get('employer', {}).get('name', ''),  # Название компании
                    'salary_from': salary_from,  # Нижняя граница зарплаты
                    'salary_to': salary_to,  # Верхняя граница зарплаты
                    'salary_currency': salary_currency,  # Валюта зарплаты
                    'region': vacancy_data.get('area', {}).get('name', ''),  # Регион
                    'publication_date': item.get('published_at', '')  # Дата публикации
                })

            except Exception as e:
                # Логируем ошибку, если обработка вакансии завершилась неудачно
                print(f"Error processing vacancy {item.get('id', '')}: {e}")

        # Если больше нет вакансий или достигнут лимит, выходим из цикла
        if not data.get('items'):
            break

        if len(vacancies) >= 10:  # Лимит на 10 вакансий
            break

        page += 1  # Переход к следующей странице

    return vacancies  # Возвращаем список вакансий

# Представление Django для отображения последних вакансий
def last_vacancies(request):
    profession = 'C/C++ программист'  # Профессия для поиска
    vacancies = get_hh_vacancies()  # Получение списка вакансий

    # Контекст данных для шаблона
    context = {'vacancies': vacancies, 'profession': profession}
    # Рендеринг HTML-шаблона с контекстом
    return render(request, 'pages/last_vacancies.html', context)
