import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def compute_vacancy_salary(entry, exchange_data):
    def fetch_exchange_rate():
        if pd.isna(entry['salary_currency']):
            return np.nan

        exchange_row = exchange_data[exchange_data['date'] == entry['month']]
        if entry['salary_currency'] not in exchange_row.columns:
            return np.nan

        return exchange_row[entry['salary_currency']].values[0] if not exchange_row.empty else np.nan

    salary = (entry['salary_from'] + entry['salary_to']) / 2 if pd.notna(entry['salary_from']) and pd.notna(
        entry['salary_to']) else \
        entry['salary_from'] if pd.notna(entry['salary_from']) else entry['salary_to']

    adjusted_salary = salary * fetch_exchange_rate() if entry['salary_currency'] != 'RUR' else salary
    return np.nan if adjusted_salary > 10_000_000 else adjusted_salary


def process_vacancy_chunk(chunk_data):
    chunk, exchange_data = chunk_data
    chunk['published_at'] = pd.to_datetime(chunk['published_at'], utc=True)
    chunk['month'] = chunk['published_at'].dt.strftime('%Y-%m')
    chunk['adjusted_salary'] = chunk.apply(lambda entry: compute_vacancy_salary(entry, exchange_data), axis=1)
    return chunk


def process_vacancy_data(vacancy_file, exchange_file):
    exchange_data = pd.read_csv(exchange_file)
    reader = pd.read_csv(vacancy_file, encoding='utf-8-sig', low_memory=False,
                         usecols=['published_at', 'salary_from', 'salary_to', 'salary_currency', 'area_name'],
                         chunksize=500_000)

    with ProcessPoolExecutor() as executor:
        processed_chunks = list(executor.map(process_vacancy_chunk, [(chunk, exchange_data) for chunk in reader]))

    df = pd.concat(processed_chunks, ignore_index=True)
    total_vacancies = 6915298
    significant_cities = df['area_name'].value_counts()[lambda x: x > total_vacancies * 0.01].index
    city_salaries = df[df['area_name'].isin(significant_cities)].groupby('area_name')[
        'adjusted_salary'].mean().round().sort_values(ascending=False)

    return city_salaries.head(10)


# Функция для сохранения данных о зарплатах по городам в HTML
def save_vacancy_to_html(city_salaries):
    # Преобразуем данные в DataFrame и задаем заголовок на русском
    city_salaries_df = city_salaries.reset_index()
    city_salaries_df.columns = ['Город', 'Средняя зарплата (руб.)']

    # Преобразуем данные в HTML таблицу
    html_table = city_salaries_df.to_html(
        index=False,
        border=1,
        table_id='salary_table',
        classes='table table-dark'
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

    # Добавляем CSS перед таблицей
    html_table = style + html_table

    # Путь для сохранения HTML файла
    html_file_path = 'data/salary_by_city.html'

    # Создание папки, если она не существует
    os.makedirs(os.path.dirname(html_file_path), exist_ok=True)

    # Сохранение таблицы в HTML файл
    with open(html_file_path, 'w', encoding='utf-8-sig') as file:
        file.write(html_table)



def plot_vacancy_salary_distribution(city_salaries):
    sorted_salaries = city_salaries.sort_values(ascending=True)

    plt.style.use('ggplot')

    plt.figure(figsize=(12, 8), facecolor='none')
    plt.barh(sorted_salaries.index, sorted_salaries.values, color='#9b59b6')

    plt.title('Средняя зарплата по городом', fontsize=20, fontname='Arial', color='black')
    plt.xlabel('Средняя зарплата (руб.)', fontsize=14, fontname='Arial', color='black')
    plt.ylabel('Города', fontsize=14, fontname='Arial', color='black')

    plt.xticks(color='black')
    plt.yticks(color='black')

    plt.grid(color='gray', linestyle='--', linewidth=0.5)

    os.makedirs('data/img', exist_ok=True)
    plt.tight_layout()

    plt.savefig('data/img/salary_by_city.png', transparent=True)
    plt.close()

    save_vacancy_to_html(sorted_salaries)


def main():
    vacancy_file = '../../../data/vacancies_2024.csv'
    exchange_file = '../../../data/currency.csv'
    city_salaries = process_vacancy_data(vacancy_file, exchange_file)
    plot_vacancy_salary_distribution(city_salaries)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
