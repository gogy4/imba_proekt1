import xml.etree.ElementTree as ET
from decimal import Decimal
from itertools import product
import pandas as pd
import requests

# Список валют, которые будем извлекать из ответа
currency_codes = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']


# Функция для получения и обработки данных за конкретный месяц и год
def get_currency_data(year, month):
    # Выполняем GET-запрос к API
    response = requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{month}/{str(year)}")
    # Преобразуем XML-ответ в дерево
    root = ET.fromstring(response.content)

    # Инициализируем словарь с датой
    monthly_data = {'date': f'{year}-{month}'}

    # Перебираем все валюты в XML
    for currency in root.findall("Valute"):
        # Получаем буквенный код валюты (например, USD, EUR)
        currency_code = currency.find("CharCode").text

        # Пропускаем валюты, которых нет в списке currency_codes
        if currency_code in currency_codes:
            # Извлекаем значение и номинал валюты
            value = Decimal(currency.find("Value").text.replace(',', '.'))
            nominal = Decimal(currency.find("Nominal").text)

            # Рассчитываем реальную стоимость одной единицы валюты и добавляем в словарь
            monthly_data[currency_code] = value / nominal

    # Возвращаем словарь с данными за месяц
    return monthly_data


# Генерация всех комбинаций года и месяца с 2003 по 2024
time_periods = [(year, f'{month:02}') for year, month in product(range(2003, 2025), range(1, 13))
                if not (year == 2024 and month == 12)]  # Исключаем декабрь 2024

# Список для хранения данных за все месяцы
all_currency_data = []

# Получаем данные за каждый месяц и добавляем в список
for year, month in time_periods:
    all_currency_data.append(get_currency_data(year, month))

# Преобразуем список словарей в DataFrame pandas
currency_df = pd.DataFrame(all_currency_data)

# Сохраняем DataFrame в CSV-файл
currency_df.to_csv('../data/currency.csv', index=False)

