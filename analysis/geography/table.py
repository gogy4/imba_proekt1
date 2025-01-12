import pandas as pd
import os
import numpy as np


# Функция для обработки данных по городам
def analyze_city_data(vacancy_data_path):
    # Чтение CSV данных
    df = pd.read_csv(vacancy_data_path,
                     encoding='utf-8-sig',
                     low_memory=False,
                     usecols=['area_name'])

    # Подсчет вакансий по городам
    city_vacancy_count = df['area_name'].value_counts()

    # Расчет доли вакансий по городам
    total_vacancies = city_vacancy_count.sum()
    city_share = city_vacancy_count / total_vacancies

    # Фильтрация городов с более чем 1% вакансий
    top_cities = city_share[city_share > 0.01]

    # Сортировка по доле вакансий и выбор топ-10 городов
    top_10_cities = top_cities.nlargest(10)

    # Расчет доли для категории "Другие"
    other_share = 1 - top_10_cities.sum()

    # Добавление категории "Другие"
    top_10_cities['Другие'] = other_share

    return top_10_cities


# Функция для сохранения данных о городах в HTML файл
def export_city_share_to_html(city_share_df):
    # Преобразуем данные в HTML таблицу
    html_table = city_share_df.to_frame('Доля вакансий Backend-программист').to_html(
        index=True,
        border=1,
        classes='table table-dark',
        float_format='{:.1%}'.format
    )

    # Путь для сохранения HTML файла
    html_file_path = 'data/city_shares.html'

    # Создание папки, если она не существует
    os.makedirs(os.path.dirname(html_file_path), exist_ok=True)

    # Сохранение таблицы в HTML файл
    with open(html_file_path, 'w', encoding='utf-8-sig') as file:
        file.write(html_table)


# Функция для вычисления зарплаты с учетом курса валют
def compute_salary(row, currency_data):
    # Получение курса валюты
    def fetch_currency_rate():
        date = row['month']
        currency = row['salary_currency']
        if currency in currency_data.columns:
            currency_row = currency_data.loc[currency_data['date'] == date]
            return currency_row[currency].values[0] if not currency_row.empty else np.nan
        return np.nan

    # Обработка пустых значений в зарплатах
    if pd.isna(row['salary_from']) and pd.isna(row['salary_to']):
        return np.nan

    # Определяем среднюю зарплату, если только одно значение указано
    if pd.isna(row['salary_from']):
        salary = row['salary_to']
    elif pd.isna(row['salary_to']):
        salary = row['salary_from']
    else:
        # Если указаны оба значения, используем среднее значение
        salary = (row['salary_from'] + row['salary_to']) / 2

    # Преобразование зарплаты в указанную валюту
    exchange_rate = fetch_currency_rate()
    converted_salary = salary * exchange_rate if row['salary_currency'] != 'RUR' else salary

    # Проверка на максимально возможную зарплату
    return np.nan if converted_salary > 10_000_000 else converted_salary


# Функция для обработки данных по зарплатам с учетом валют
def analyze_salary_data(vacancy_data_path, currency_data_path):
    # Загрузка данных о курсах валют
    currency_data = pd.read_csv(currency_data_path)

    # Чтение данных о вакансиях
    df = pd.read_csv(vacancy_data_path,
                     encoding='utf-8-sig',
                     low_memory=False,
                     usecols=['published_at', 'salary_from', 'salary_to', 'salary_currency', 'area_name'])

    # Обработка даты для извлечения месяца
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True)
    df['month'] = df['published_at'].dt.strftime('%Y-%m')

    # Применение вычисления зарплаты с учетом курсов валют
    df['adjusted_salary'] = df.apply(
        lambda row: compute_salary(row, currency_data),
        axis=1
    )

    # Подсчет общего числа вакансий
    total_vacancies_count = len(df)

    # Фильтрация по количеству вакансий по городам
    city_vacancy_counts = df['area_name'].value_counts()
    relevant_cities = city_vacancy_counts[city_vacancy_counts > total_vacancies_count * 0.01].index

    # Расчет средней зарплаты по городам
    city_avg_salary = df[df['area_name'].isin(relevant_cities)].groupby('area_name')[
        'adjusted_salary'].mean().round().sort_values(ascending=False)

    return city_avg_salary.head(10)


# Функция для сохранения данных о зарплатах в HTML
def export_city_salaries_to_html(city_avg_salary_df):
    # Путь для сохранения HTML файла
    salary_html_path = 'data/city_salaries.html'

    # Создание папки, если она не существует
    os.makedirs(os.path.dirname(salary_html_path), exist_ok=True)

    city_avg_salary_df.to_frame().to_html(salary_html_path,
                                          table_id='salary_table',
                                          classes='table table-dark')


# Основная функция, которая обрабатывает данные и сохраняет результаты
def main():
    # Пути к файлам
    vacancy_data_path = 'data/vacancies_by_name.csv'
    currency_data_path = 'data/currency.csv'

    # Получение данных о доле вакансий по городам
    city_share = analyze_city_data(vacancy_data_path)

    # Сохранение таблицы о доле вакансий по городам в HTML
    export_city_share_to_html(city_share)

    # Получение данных о средней зарплате по городам
    city_avg_salary = analyze_salary_data(vacancy_data_path, currency_data_path)

    # Сохранение таблицы о средней зарплате по городам в HTML
    export_city_salaries_to_html(city_avg_salary)


# Запуск основной функции
if __name__ == '__main__':
    main()
