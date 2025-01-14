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


def save_vacancy_to_html(city_salaries):
    os.makedirs('data', exist_ok=True)

    city_salaries_df = city_salaries.reset_index()
    city_salaries_df.columns = ['City', 'Average Salary (rub.)']

    html = city_salaries_df.to_html(index=False, border=1, classes='table table-dark', header=True)

    html = html.replace('<table', '<table style="width: 60%; margin-left: auto; margin-right: auto; border-collapse: collapse;"')

    html = html.replace('<td>', '<td style="text-align: center;">')
    html = html.replace('<th>', '<th style="text-align: center;">')

    with open('data/salary_by_city.html', 'w', encoding='utf-8-sig') as f:
        f.write(html)


def plot_vacancy_salary_distribution(city_salaries):
    sorted_salaries = city_salaries.sort_values(ascending=True)

    plt.style.use('ggplot')

    plt.figure(figsize=(12, 8), facecolor='none')
    plt.barh(sorted_salaries.index, sorted_salaries.values, color='#9b59b6')

    plt.title('Average Salary by City', fontsize=20, fontname='Arial', color='black')
    plt.xlabel('Average Salary (rub.)', fontsize=14, fontname='Arial', color='black')
    plt.ylabel('Cities', fontsize=14, fontname='Arial', color='black')

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
