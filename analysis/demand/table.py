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

# Функция для сохранения вакансий в HTML с кастомным стилем
def save_vacancies_to_html(vacancies_df):
    os.makedirs('data', exist_ok=True)

    # Преобразуем данные в DataFrame и задаем заголовок на русском
    vacancies_df = vacancies_df.reset_index()
    vacancies_df.columns = ['Год', 'Количество вакансий']

    # Преобразуем данные в HTML таблицу
    html_table = vacancies_df.to_html(
        index=False,
        border=1,
        table_id='vacancies_table',
        classes='table table-dark'
    )

    # Добавляем CSS для кастомного дизайна
    style = """
    <style>
        #vacancies_table {
            background-color: #7766cf; /* skypurple */
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 15px;
            overflow: hidden;
        }
        #vacancies_table th, #vacancies_table td {
            text-align: center;
            border: 1px solid #594f99;
            padding: 10px;
        }
        #vacancies_table th {
            background-color: #594f99;
            color: white;
        }
        #vacancies_table td {
            color: white;
        }
    </style>
    """

    # Добавляем CSS перед таблицей
    html_table = style + html_table

    # Сохранение таблицы в HTML файл
    with open('data/vacancies_by_year.html', 'w', encoding='utf-8-sig') as f:
        f.write(html_table)

# Функция для расчета и конвертации зарплаты
def convert_salary(row, currency_data):
    def get_exchange_rate():
        date = row['month']
        currency = row['salary_currency']
        if currency in currency_data.columns:
            rate_row = currency_data.loc[currency_data['date'] == date]
            return rate_row[currency].values[0] if not rate_row.empty else np.nan
        return np.nan

    if pd.isna(row['salary_from']) and pd.isna(row['salary_to']):
        return np.nan

    if pd.isna(row['salary_from']):
        salary = row['salary_to']
    elif pd.isna(row['salary_to']):
        salary = row['salary_from']
    else:
        salary = (row['salary_from'] + row['salary_to']) / 2

    exchange_rate = get_exchange_rate()
    converted_salary = salary * exchange_rate if row['salary_currency'] != 'RUR' else salary

    return np.nan if converted_salary > 10_000_000 else converted_salary

# Функция для обработки зарплат по годам
def process_salary_by_year(file_path, currency_file_path):
    currency_data = pd.read_csv(currency_file_path)

    df = pd.read_csv(file_path,
                     encoding='utf-8-sig',
                     low_memory=False,
                     usecols=['published_at', 'salary_from', 'salary_to', 'salary_currency'])

    df['published_at'] = pd.to_datetime(df['published_at'], utc=True)
    df['year'] = df['published_at'].dt.year
    df['month'] = df['published_at'].dt.strftime('%Y-%m')

    df['converted_salary'] = df.apply(
        lambda row: convert_salary(row, currency_data),
        axis=1
    )

    average_salaries_per_year = df.groupby('year')['converted_salary'].mean().round()

    return average_salaries_per_year

# Функция для сохранения данных о зарплатах в HTML с кастомным стилем
def save_salary_to_html(average_salaries):
    average_salaries = average_salaries.reset_index()
    average_salaries.columns = ['Год', 'Средняя зарплата']

    html_table = average_salaries.to_html(
        index=False,
        border=1,
        table_id='salary_table',
        classes='table table-dark',
        float_format='{:,.0f}'.format
    )

    style = """
    <style>
        #salary_table {
            background-color: #7766cf; /* skypurple */
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 15px;
            overflow: hidden;
        }
        #salary_table th, #salary_table td {
            text-align: center;
            border: 1px solid #594f99;
            padding: 10px;
        }
        #salary_table th {
            background-color: #594f99;
            color: white;
        }
        #salary_table td {
            color: white;
        }
    </style>
    """

    html_table = style + html_table

    with open('data/salary_by_year.html', 'w', encoding='utf-8') as f:
        f.write(html_table)

# Главная функция
def run_analysis():
    file_path = '../../data/vacancies_by_name.csv'
    currency_file_path = '../../data/currency.csv'

    vacancies_by_year = count_vacancies_by_year(file_path)
    save_vacancies_to_html(vacancies_by_year)

    salaries_by_year = process_salary_by_year(file_path, currency_file_path)
    save_salary_to_html(salaries_by_year)

if __name__ == '__main__':
    run_analysis()
