import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def compute_salary(row, exchange_rate_data):
    # Получение курса валюты
    def fetch_exchange_rate():
        date = row['month']
        currency = row['salary_currency']
        if currency in exchange_rate_data.columns:
            rate_row = exchange_rate_data.loc[exchange_rate_data['date'] == date]
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
    exchange_rate = fetch_exchange_rate()
    converted_salary = salary * exchange_rate if row['salary_currency'] != 'RUR' else salary

    # Проверка на максимальную зарплату
    return np.nan if converted_salary > 10_000_000 else converted_salary


def analyze_vacancies_and_salaries(vacancies_file, currency_file):
    # Загрузка данных о валютных курсах
    exchange_data = pd.read_csv(currency_file)

    # Чтение данных о вакансиях
    vacancies_df = pd.read_csv(vacancies_file,
                               encoding='utf-8-sig',
                               low_memory=False,
                               usecols=['published_at', 'salary_from', 'salary_to', 'salary_currency', 'area_name'])

    # Обработка даты
    vacancies_df['published_at'] = pd.to_datetime(vacancies_df['published_at'], utc=True)
    vacancies_df['month'] = vacancies_df['published_at'].dt.strftime('%Y-%m')

    # Применяем расчет зарплаты с передачей курсов валют
    vacancies_df['adjusted_salary'] = vacancies_df.apply(
        lambda row: compute_salary(row, exchange_data),
        axis=1
    )

    # Расчет общего числа вакансий
    total_vacancies = len(vacancies_df)

    # Фильтрация по городам с более чем 1% вакансий
    city_vacancies = vacancies_df['area_name'].value_counts()
    significant_cities = city_vacancies[city_vacancies > total_vacancies * 0.01].index

    # Расчет средней зарплаты по городам
    city_avg_salaries = vacancies_df[vacancies_df['area_name'].isin(significant_cities)].groupby('area_name')[
        'adjusted_salary'].mean().round().sort_values(ascending=False)

    # Расчет доли вакансий по городам
    total_vacancies_by_city = vacancies_df['area_name'].value_counts()
    total_vacancies_count = total_vacancies_by_city.sum()
    city_shares = total_vacancies_by_city / total_vacancies_count

    # Фильтрация городов с более чем 1% вакансий
    significant_city_shares = city_shares[city_shares > 0.01]

    # Сортировка по доле вакансий и выбор топ-10
    top_10_city_shares = significant_city_shares.nlargest(10)

    # Расчет доли "Другие"
    other_share = 1 - top_10_city_shares.sum()

    # Добавление категории "Другие"
    top_10_city_shares['Другие'] = other_share

    return city_avg_salaries.head(10), top_10_city_shares


def plot_average_salaries_by_city(city_avg_salaries):
    # Сортировка данных для визуализации по убыванию
    sorted_salaries = city_avg_salaries.sort_values(ascending=False)

    plt.figure(figsize=(12, 8), facecolor='white')  # Белый фон для графика
    ax = plt.gca()
    ax.set_facecolor('white')  # Белый фон для осей

    # Новый набор цветов с фиолетовыми и синими оттенками
    colors = [
        '#6A0DAD',  # Ярко-фиолетовый
        '#9B4F96',  # Лаванда
        '#8A2BE2',  # Синий с фиолетовым оттенком
        '#7A1FA2',  # Темный фиолетовый
        '#9C27B0',  # Яркий пурпурный
        '#6A5ACD',  # Средний синий
        '#BA55D3',  # Средний фиолетовый
        '#4B0082',  # Индиго
        '#483D8B',  # Темно-синий
        '#8B00FF',  # Пурпурный
        '#4169E1',  # Королевский синий
        '#663399',  # Фиолетовый цвет
        '#1E90FF',  # Додж-блю
        '#B0C4DE',  # Светлый стальной синий
        '#0000CD'   # Темно-синий
    ]

    plt.barh(sorted_salaries.index, sorted_salaries.values, color=colors[:len(sorted_salaries)])

    # Инвертируем ось Y, чтобы самое большое значение было сверху
    plt.gca().invert_yaxis()

    plt.title('Средняя зарплата по городам для C/C++ программистов', fontsize=20, color='#9b59b6')  # Фиолетовый цвет для заголовка
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.xlabel('Средняя зарплата (руб.)', fontsize=14)

    # Сохранение графика в папку static_dev/geography/img
    output_dir = 'data/img'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.tight_layout()
    output_path = os.path.join(output_dir, 'salary_by_city.png')
    plt.savefig(output_path)
    plt.close()


def plot_vacancy_shares_by_city(top_10_city_shares):
    # Устанавливаем стиль белого фона
    plt.figure(figsize=(12, 8), facecolor='white')  # Белый фон

    # Новый набор цветов с фиолетовыми и синими оттенками
    colors = [
        '#6A0DAD',  # Ярко-фиолетовый
        '#9B4F96',  # Лаванда
        '#8A2BE2',  # Синий с фиолетовым оттенком
        '#7A1FA2',  # Темный фиолетовый
        '#9C27B0',  # Яркий пурпурный
        '#6A5ACD',  # Средний синий
        '#BA55D3',  # Средний фиолетовый
        '#4B0082',  # Индиго
        '#483D8B',  # Темно-синий
        '#8B00FF',  # Пурпурный
        '#4169E1',  # Королевский синий
        '#663399',  # Фиолетовый цвет
        '#1E90FF',  # Додж-блю
        '#B0C4DE',  # Светлый стальной синий
        '#0000CD'   # Темно-синий
    ]

    # График доли вакансий по городам
    plt.pie(top_10_city_shares, labels=top_10_city_shares.index, autopct='%1.1f%%',
            textprops={'fontsize': 10, 'color': 'white'},  # Изменен цвет шрифта процента на белый
            colors=colors[:len(top_10_city_shares)])

    plt.title('Доля вакансий по городам для C/C++ программистов', fontsize=24, color='#9b59b6')  # Фиолетовый цвет для заголовка

    # Сохранение графика в папку static_dev/geography/img
    output_dir = 'data/img'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.tight_layout()
    output_path = os.path.join(output_dir, 'vacancy_by_city.png')
    plt.savefig(output_path)
    plt.close()


def main():
    # Пути к файлам
    vacancies_file = '../../data/vacancies_by_name.csv'
    currency_file = '../../data/currency.csv'

    # Получение результатов
    city_avg_salaries, top_10_city_shares = analyze_vacancies_and_salaries(vacancies_file, currency_file)

    # Построение графиков
    plot_average_salaries_by_city(city_avg_salaries)
    plot_vacancy_shares_by_city(top_10_city_shares)


if __name__ == '__main__':
    main()
