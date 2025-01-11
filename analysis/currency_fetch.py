import xml.etree.ElementTree as ET
from decimal import Decimal

import pandas as pd
import requests

# фильтраж колонок для запроса
headers = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']

result = []
# гениально-программистский перебор
for year in range(2003, 2025):
    for month in ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'):
        # запрос взят с api, возвращает валюты на месяц
        response = requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{month}/{str(year)}")
        root = ET.fromstring(response.content)

        # словарик для валют месяца
        month_data = {
            'date': f'{str(year)}-{month}',
        }

        for valute in root.findall("Valute"):
            # чтобы не перебирать кучу ненужных валют
            if valute.find("CharCode").text not in headers:
                continue
            # валюта = значение / номинал
            month_data[valute.find("CharCode").text] = (Decimal(valute.find("Value").text.replace(',', '.'))
                                                        / Decimal(valute.find("Nominal").text))

        result.append(month_data)

df = pd.DataFrame(result)
df.to_csv('data/currency.csv', index=False)