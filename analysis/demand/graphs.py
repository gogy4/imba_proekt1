import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# Функция для подсчета вакансий по годам
def count_vacancies_by_year(file_path):
    # Чтение CSV
    df = pd.read_csv(file_path,
                     encoding='utf-8-sig',
                     low_memory=False,
                     usecols=['published_at'])

    # Преобразование даты и подсчет вакансий по годам
    df['year'] = pd.to_datetime(df['published_at'], utc=True).dt.year
    total_vacancies_by_year = df['year'].value_counts().sort_index()

    return total_vacancies_by_year

# Функция для построения графика по количеству вакансий
def plot_vacancy_counts(years, counts):
    # Устанавливаем стиль для графика
    plt.style.use('fivethirtyeight')  # Используем стиль 'fivethirtyeight'

    # Создание фигуры и подграфиков
    plt.figure(figsize=(12, 8))

    # Позиции по оси X
    x = np.arange(len(years))
    width = 0.5

    # График количества вакансий по годам
    bars = plt.bar(x, counts, width, label='Количество вакансий C/C++ программист', color='#9b59b6')  # фиолетовый цвет

    # Добавление значений над столбцами
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval),
                 ha='center', va='bottom', color='white', fontsize=10)

    # Настройка заголовка и меток осей
    plt.title('Количество вакансий по годам C/C++ программист', fontsize=16, color='#9b59b6')
    plt.xticks(x, years, rotation=90, fontsize=12, color='#8e44ad')
    plt.ylabel('Количество вакансий', fontsize=12, color='#8e44ad')
    plt.legend(fontsize=10, facecolor='#9b59b6', edgecolor='white')
    plt.grid(True, axis='y', color='gray', linestyle='--', alpha=0.5)

    # Сохранение графика в файл с белым фоном
    os.makedirs('data/img', exist_ok=True)  # Создание папки, если ее нет
    plt.tight_layout()
    plt.savefig('data/img/vacancy_by_year.png', bbox_inches='tight', facecolor='white')
    plt.close()  # Закрываем figure

# Функция для расчета зарплаты с учетом валют
def compute_salary(row, currency_data):
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
def process_salaries_by_year(file_path, currency_file_path):
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
        lambda row: compute_salary(row, currency_data),
        axis=1
    )

    # Расчет средней зарплаты по годам
    avg_salaries_by_year = df.groupby('year')['converted_salary'].mean().round()

    return avg_salaries_by_year

# Функция для построения графика средней зарплаты по годам
def plot_avg_salary_by_year(avg_salaries_by_year):
    plt.style.use('fivethirtyeight')  # Используем стиль 'fivethirtyeight'

    # Создание фигуры
    plt.figure(figsize=(12, 8))

    plt.bar(avg_salaries_by_year.index.astype(str), avg_salaries_by_year.values,
            label='Средняя з/п', color='#9b59b6')  # фиолетовый цвет

    plt.title('Уровень зарплат по годам C/C++ программист', fontsize=20, color='#9b59b6')
    plt.ylabel('Средняя з/п', fontsize=14, color='#8e44ad')
    plt.xticks(rotation=45, fontsize=12, color='#8e44ad')
    plt.legend(fontsize=14, facecolor='#9b59b6', edgecolor='white')
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    plt.tight_layout()

    # Сохранение графика с белым фоном
    os.makedirs('data/img', exist_ok=True)  # Создание папки, если ее нет
    plt.savefig('data/img/salary_by_year.png', bbox_inches='tight', facecolor='white')
    plt.close()  # Закрываем figure

# Главная функция
def execute_analysis():
    # Пути к файлам
    file_path = '../../data/vacancies_by_name.csv'
    currency_file_path = '../../data/currency.csv'

    # Получение результатов по вакансиям
    yearly_vacancies = count_vacancies_by_year(file_path)

    # Построение графика для количества вакансий
    plot_vacancy_counts(yearly_vacancies.index, yearly_vacancies.values)

    # Получение результатов по зарплатам
    avg_salaries_by_year = process_salaries_by_year(file_path, currency_file_path)

    # Построение графика для средней зарплаты
    plot_avg_salary_by_year(avg_salaries_by_year)

if __name__ == '__main__':
    execute_analysis()
