import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


# Функция для подсчета вакансий по годам
def count_vacancies_by_year(file_path):
    # Чтение данных из CSV файла, использование только колонки 'published_at'
    df = pd.read_csv(file_path, encoding='utf-8-sig', low_memory=False, usecols=['published_at'])

    # Преобразование даты публикации вакансии в год
    df['year'] = pd.to_datetime(df['published_at'], utc=True).dt.year

    # Подсчет количества вакансий по годам
    total_vacancies_by_year = df['year'].value_counts().sort_index()
    return total_vacancies_by_year


# Функция для построения графика по количеству вакансий
def plot_vacancy_counts(years, counts):
    # Используем стиль 'fivethirtyeight' для графика
    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(12, 8))

    # Создаем бары для отображения количества вакансий по годам
    x = np.arange(len(years))
    width = 0.5

    # Строим столбчатую диаграмму
    bars = plt.bar(x, counts, width, label='Количество вакансий C/C++ программист', color='#9b59b6')

    # Добавляем значения над столбцами
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval),
                 ha='center', va='bottom', color='black', fontsize=10)

    # Настройки графика
    plt.title('Количество вакансий по годам C/C++ программист', fontsize=16, color='black')
    plt.xticks(x, years, rotation=90, fontsize=12, color='black')
    plt.ylabel('Количество вакансий', fontsize=12, color='black')
    plt.legend(fontsize=10, facecolor='white', edgecolor='black', labelcolor='black')
    plt.grid(True, axis='y', color='gray', linestyle='--', alpha=0.5)

    # Сохраняем график в файл
    os.makedirs('data/img', exist_ok=True)
    plt.tight_layout()
    plt.savefig('data/img/vacancy_by_year.png', bbox_inches='tight', transparent=True)
    plt.close()


# Функция для расчета зарплаты с учетом валют
def compute_salary(row, currency_data):
    # Функция для получения курса валюты на месяц
    def get_exchange_rate():
        # Извлекаем дату из строки (месяц, для которого нужно получить курс валюты)
        date = row['month']
        # Извлекаем валюту из строки, в которой указана валюта зарплаты
        currency = row['salary_currency']

        # Если валюта есть в данных о курсах валют (столбцы должны соответствовать валютам),
        # то ищем строку с нужной датой
        if currency in currency_data.columns:
            # Ищем строки в данных о курсах валют, где дата совпадает с месяцем из строки
            rate_row = currency_data.loc[currency_data['date'] == date]

            # Если строка с курсом найдена, возвращаем курс для данной валюты
            # Иначе, если строка пустая, возвращаем NaN
            return rate_row[currency].values[0] if not rate_row.empty else np.nan

        # Если валюты нет в данных о курсах, возвращаем NaN
        return np.nan

    # Проверяем, если данные о зарплате отсутствуют (и salary_from, и salary_to равны NaN),
    # то сразу возвращаем NaN, так как нечего рассчитывать
    if pd.isna(row['salary_from']) and pd.isna(row['salary_to']):
        return np.nan

    # Если одна из составляющих зарплаты отсутствует (например, salary_from или salary_to),
    # то считаем, что зарплата равна другой составляющей
    if pd.isna(row['salary_from']):
        salary = row['salary_to']
    elif pd.isna(row['salary_to']):
        salary = row['salary_from']
    else:
        # Если обе составляющие зарплаты присутствуют, то считаем среднее значение
        salary = (row['salary_from'] + row['salary_to']) / 2

    # Получаем курс валюты для выбранного месяца и валюты
    exchange_rate = get_exchange_rate()

    # Если валюта зарплаты не рубли, то конвертируем зарплату по найденному курсу
    # Если валюта уже рубли, то оставляем зарплату без изменений
    converted_salary = salary * exchange_rate if row['salary_currency'] != 'RUR' else salary

    # Если конвертированная зарплата слишком велика (больше 10 миллионов), возвращаем NaN,
    # так как такие значения могут быть ошибочными или некорректными
    return np.nan if converted_salary > 10_000_000 else converted_salary


# Функция для обработки зарплат по годам
def process_salaries_by_year(file_path, currency_file_path):
    # Чтение данных о валютных курсах и вакансиях
    currency_data = pd.read_csv(currency_file_path)
    df = pd.read_csv(file_path, encoding='utf-8-sig', low_memory=False,
                     usecols=['published_at', 'salary_from', 'salary_to', 'salary_currency'])

    # Преобразование даты в формат datetime
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True)

    # Добавляем столбцы для года и месяца
    df['year'] = df['published_at'].dt.year
    df['month'] = df['published_at'].dt.strftime('%Y-%m')

    # Применяем функцию для расчета зарплаты с учетом валют
    df['converted_salary'] = df.apply(
        lambda row: compute_salary(row, currency_data),
        axis=1
    )

    # Рассчитываем среднюю зарплату по годам
    avg_salaries_by_year = df.groupby('year')['converted_salary'].mean().round()
    return avg_salaries_by_year


# Функция для построения графика средней зарплаты по годам
def plot_avg_salary_by_year(avg_salaries_by_year):
    # Используем стиль 'fivethirtyeight' для графика
    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(12, 8))

    # Строим столбчатую диаграмму для средней зарплаты
    plt.bar(avg_salaries_by_year.index.astype(str), avg_salaries_by_year.values,
            label='Средняя з/п', color='#9b59b6')

    # Настройки графика
    plt.title('Уровень зарплат по годам C/C++ программист', fontsize=20, color='black')
    plt.ylabel('Средняя з/п', fontsize=14, color='black')
    plt.xticks(rotation=45, fontsize=12, color='black')
    plt.legend(fontsize=14, facecolor='white', edgecolor='black', labelcolor='black')
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    plt.tight_layout()

    # Сохраняем график в файл
    os.makedirs('data/img', exist_ok=True)
    plt.savefig('data/img/salary_by_year.png', bbox_inches='tight', transparent=True)
    plt.close()


# Главная функция
def execute_analysis():
    # Путь к файлам данных
    file_path = '../../data/vacancies_by_name.csv'
    currency_file_path = '../../data/currency.csv'

    # Анализируем количество вакансий и строим график
    yearly_vacancies = count_vacancies_by_year(file_path)
    plot_vacancy_counts(yearly_vacancies.index, yearly_vacancies.values)

    # Анализируем зарплаты и строим график
    avg_salaries_by_year = process_salaries_by_year(file_path, currency_file_path)
    plot_avg_salary_by_year(avg_salaries_by_year)


# Запуск анализа, если скрипт выполняется напрямую
if __name__ == '__main__':
    execute_analysis()
