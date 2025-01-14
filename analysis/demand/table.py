import pandas as pd
import numpy as np
import os

# Функция для подсчета количества вакансий по годам
def count_vacancies_by_year(file_path):
    # Чтение CSV файла, используя только колонку 'published_at'
    df = pd.read_csv(file_path,
                     encoding='utf-8-sig',
                     low_memory=False,
                     usecols=['published_at'])

    # Преобразование столбца 'published_at' в дату и подсчет вакансий по годам
    df['year'] = pd.to_datetime(df['published_at'], utc=True).dt.year
    vacancies_per_year = df['year'].value_counts().sort_index()

    return vacancies_per_year

# Функция для сохранения вакансий в HTML с кастомным стилем
def save_vacancies_to_html(vacancies_df):
    # Создаем папку для хранения данных, если она не существует
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

    # Добавляем CSS для кастомного дизайна таблицы
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

    # Добавляем стили перед таблицей
    html_table = style + html_table

    # Сохраняем таблицу в HTML файл
    with open('data/vacancies_by_year.html', 'w', encoding='utf-8-sig') as f:
        f.write(html_table)

# Функция для расчета и конвертации зарплаты
def convert_salary(row, currency_data):
    # Функция для получения курса валюты на месяц
    def get_exchange_rate():
        date = row['month']
        currency = row['salary_currency']
        if currency in currency_data.columns:
            rate_row = currency_data.loc[currency_data['date'] == date]
            return rate_row[currency].values[0] if not rate_row.empty else np.nan
        return np.nan

    # Если данные о зарплате отсутствуют, возвращаем NaN
    if pd.isna(row['salary_from']) and pd.isna(row['salary_to']):
        return np.nan

    # Рассчитываем среднюю зарплату, если один из параметров отсутствует
    if pd.isna(row['salary_from']):
        salary = row['salary_to']
    elif pd.isna(row['salary_to']):
        salary = row['salary_from']
    else:
        salary = (row['salary_from'] + row['salary_to']) / 2

    # Получаем курс валюты и преобразуем зарплату
    exchange_rate = get_exchange_rate()
    converted_salary = salary * exchange_rate if row['salary_currency'] != 'RUR' else salary

    # Возвращаем NaN, если зарплата слишком велика
    return np.nan if converted_salary > 10_000_000 else converted_salary

# Функция для обработки зарплат по годам
def process_salary_by_year(file_path, currency_file_path):
    # Чтение данных о курсах валют и вакансиях
    currency_data = pd.read_csv(currency_file_path)

    df = pd.read_csv(file_path,
                     encoding='utf-8-sig',
                     low_memory=False,
                     usecols=['published_at', 'salary_from', 'salary_to', 'salary_currency'])

    # Преобразуем дату в формат datetime
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True)

    # Добавляем столбцы для года и месяца
    df['year'] = df['published_at'].dt.year
    df['month'] = df['published_at'].dt.strftime('%Y-%m')

    # Применяем функцию для расчета зарплаты с учетом валют
    df['converted_salary'] = df.apply(
        lambda row: convert_salary(row, currency_data),
        axis=1
    )

    # Рассчитываем среднюю зарплату по годам
    average_salaries_per_year = df.groupby('year')['converted_salary'].mean().round()

    return average_salaries_per_year

# Функция для сохранения данных о зарплатах в HTML с кастомным стилем
def save_salary_to_html(average_salaries):
    # Преобразуем данные в DataFrame
    average_salaries = average_salaries.reset_index()
    average_salaries.columns = ['Год', 'Средняя зарплата']

    # Преобразуем данные в HTML таблицу
    html_table = average_salaries.to_html(
        index=False,
        border=1,
        table_id='salary_table',
        classes='table table-dark',
        float_format='{:,.0f}'.format
    )

    # Добавляем CSS для кастомного дизайна
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

    # Добавляем стили перед таблицей
    html_table = style + html_table

    # Сохраняем таблицу в HTML файл
    with open('data/salary_by_year.html', 'w', encoding='utf-8') as f:
        f.write(html_table)

# Главная функция для выполнения анализа
def run_analysis():
    # Путь к файлам данных
    file_path = '../../data/vacancies_by_name.csv'
    currency_file_path = '../../data/currency.csv'

    # Подсчитываем количество вакансий по годам и сохраняем в HTML
    vacancies_by_year = count_vacancies_by_year(file_path)
    save_vacancies_to_html(vacancies_by_year)

    # Обрабатываем зарплаты по годам и сохраняем в HTML
    salaries_by_year = process_salary_by_year(file_path, currency_file_path)
    save_salary_to_html(salaries_by_year)

# Запуск анализа, если скрипт выполняется напрямую
if __name__ == '__main__':
    run_analysis()
