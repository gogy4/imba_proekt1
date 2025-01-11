import pandas as pd
import numpy as np
import os

# Функция для подсчета количества вакансий по годам
def count_vacancies_by_year(file_path):
    # Чтение CSV
    df = pd.read_csv(file_path,
                     encoding='utf-8-sig',
                     low_memory=False,
                     usecols=['published_at'])

    # Преобразование даты и подсчет вакансий по годам
    df['year'] = pd.to_datetime(df['published_at'], utc=True).dt.year
    vacancies_per_year = df['year'].value_counts().sort_index()

    return vacancies_per_year

# Функция для сохранения вакансий в HTML
def save_vacancies_to_html(vacancies_df):
    # Преобразуем DataFrame в HTML-таблицу
    os.makedirs('data', exist_ok=True)
    html_string = vacancies_df.to_frame().to_html(
        index=True,
        border=1,
        classes='table table-dark',
        header=['Количество вакансий']
    )
    with open('data/vacancies_by_year.html', 'w', encoding='utf-8-sig') as f:
        f.write(html_string)

# Функция для расчета и конвертации зарплаты
def convert_salary(row, currency_data):
    # Получение курса валюты
    def get_exchange_rate():
        date = row['month']
        currency = row['salary_currency']
        if currency in currency_data.columns:
            rate_row = currency_data.loc[currency_data['date'] == date]
            return rate_row[currency].values[0] if not rate_row.empty else np.nan
        return np.nan

    # Обработка зарплат с учетом null значений
    if pd.isna(row['salary_from']) and pd.isna(row['salary_to']):
        return np.nan

    if pd.isna(row['salary_from']):
        salary = row['salary_to']
    elif pd.isna(row['salary_to']):
        salary = row['salary_from']
    else:
        # Если оба значения есть, берем среднее
        salary = (row['salary_from'] + row['salary_to']) / 2

    # Конвертация валюты
    exchange_rate = get_exchange_rate()
    converted_salary = salary * exchange_rate if row['salary_currency'] != 'RUR' else salary

    # Фильтрация зарплат свыше 10 000 000
    return np.nan if converted_salary > 10_000_000 else converted_salary

# Функция для обработки зарплат по годам
def process_salary_by_year(file_path, currency_file_path):
    # Загрузка валют заранее
    currency_data = pd.read_csv(currency_file_path)

    # Чтение CSV
    df = pd.read_csv(file_path,
                     encoding='utf-8-sig',
                     low_memory=False,
                     usecols=['published_at', 'salary_from', 'salary_to', 'salary_currency'])

    # Обработка даты
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True)
    df['year'] = df['published_at'].dt.year
    df['month'] = df['published_at'].dt.strftime('%Y-%m')

    # Применяем расчет зарплаты с передачей курсов валют
    df['converted_salary'] = df.apply(
        lambda row: convert_salary(row, currency_data),
        axis=1
    )

    # Расчет средней зарплаты по годам
    average_salaries_per_year = df.groupby('year')['converted_salary'].mean().round()

    return average_salaries_per_year

# Функция для создания HTML таблицы средней зарплаты
def save_salary_to_html(average_salaries):
    # Преобразуем Series в DataFrame и создаем HTML-таблицу
    html_string = average_salaries.to_frame('Средняя зарплата').to_html(
        index=True,
        border=1,
        classes='dataframe table table-dark',
        float_format='{:,.0f}'.format  # Форматирование чисел
    )

    with open('data/average_salary_by_year.html', 'w', encoding='utf-8') as f:
        f.write(html_string)

# Главная функция
def run_analysis():
    # Пути к файлам
    file_path = 'data/vacancies_by_name.csv'
    currency_file_path = 'data/currency.csv'

    # Получение результатов по вакансиям
    vacancies_by_year = count_vacancies_by_year(file_path)
    save_vacancies_to_html(vacancies_by_year)

    # Получение результатов по зарплатам
    salaries_by_year = process_salary_by_year(file_path, currency_file_path)
    save_salary_to_html(salaries_by_year)

if __name__ == '__main__':
    run_analysis()
