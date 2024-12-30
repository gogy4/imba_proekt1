# myapp/management/commands/fetch_vacancies.py
import requests
import pandas as pd
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fetch vacancies data from HH API and save to CSV'

    def handle(self, *args, **kwargs):
        hh_api_url = "https://api.hh.ru/vacancies"
        params = {
            'text': 'C++',  # Профессия
            'per_page': 100,
            'page': 0
        }
        response = requests.get(hh_api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            vacancies = data['items']
            vacancies_list = []
            for vacancy in vacancies:
                salary_from = vacancy['salary']['from'] if vacancy['salary'] else None
                salary_to = vacancy['salary']['to'] if vacancy['salary'] else None
                salary_currency = vacancy['salary']['currency'] if vacancy['salary'] else None
                vacancies_list.append({
                    'name': vacancy['name'],
                    'salary_from': salary_from,
                    'salary_to': salary_to,
                    'salary_currency': salary_currency,
                    'published_at': vacancy['published_at']
                })
            vacancies_df = pd.DataFrame(vacancies_list)
            vacancies_df.to_csv('data/vacancies.csv', index=False)
            self.stdout.write(self.style.SUCCESS("Vacancies data saved to 'data/vacancies.csv'"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to fetch vacancies data: {response.status_code}"))
