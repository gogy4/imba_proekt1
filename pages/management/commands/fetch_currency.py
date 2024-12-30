# myapp/management/commands/fetch_currency.py
import requests
import pandas as pd
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fetch currency data from CB API and save to CSV'

    def handle(self, *args, **kwargs):
        cb_api_url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(cb_api_url)

        if response.status_code == 200:
            data = response.json()
            currencies = data['Valute']
            currency_list = []
            for currency_code, currency_info in currencies.items():
                currency_list.append({
                    'char_code': currency_info['CharCode'],
                    'name': currency_info['Name'],
                    'value': currency_info['Value'],
                    'date': data['Date'][:10]
                })
            currency_df = pd.DataFrame(currency_list)
            currency_df.to_csv('data/currency.csv', index=False)
            self.stdout.write(self.style.SUCCESS("Currency data saved to 'data/currency.csv'"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to fetch currency data: {response.status_code}"))
