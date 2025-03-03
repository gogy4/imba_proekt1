import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


def calculate_salary(row, exchange_csv):
    # Функция для получения курса обмена
    def get_exchange_rate():
        rate_row = exchange_csv[exchange_csv['date'] == row['month']]
        return rate_row[row['salary_currency']].values[0] if not rate_row.empty else np.nan

    # Если обе зарплаты пустые, возвращаем NaN
    if pd.isna(row['salary_from']) and pd.isna(row['salary_to']):
        return np.nan

    # Если одна из зарплат пустая, то берем другую, если обе заданы, то вычисляем среднее значение
    salary = row['salary_from'] if pd.isna(row['salary_to']) else row['salary_to'] if pd.isna(row['salary_from']) else (
                                                                                       row[
                                                                                           'salary_from'] +
                                                                                       row[
                                                                                           'salary_to']) / 2

    # Преобразуем зарплату в рубли, если валюта не RUR, используем курс обмена
    converted_salary = salary * get_exchange_rate() if row['salary_currency'] != 'RUR' else salary

    # Если зарплата слишком высокая, возвращаем NaN
    return np.nan if converted_salary > 10_000_000 else converted_salary


def process_data_chunk(data_chunk):
    # Обрабатываем кусок данных, применяя функцию расчета зарплаты
    chunk, exchange_csv = data_chunk
    chunk['published_at'] = pd.to_datetime(chunk['published_at'], utc=True)
    chunk['year'], chunk['month'] = chunk['published_at'].dt.year, chunk['published_at'].dt.strftime('%Y-%m')
    chunk['converted_salary'] = chunk.apply(lambda row: calculate_salary(row, exchange_csv), axis=1)
    return chunk


def process_salary_data(file_path, exchange_file_path):
    # Загружаем данные из файлов и обрабатываем их
    exchange_csv = pd.read_csv(exchange_file_path)

    # Чтение данных из файла по частям (по 500,000 строк за раз)
    reader = pd.read_csv(file_path, encoding='utf-8-sig', low_memory=False,
                         usecols=['published_at', 'salary_from', 'salary_to', 'salary_currency'], chunksize=500_000)

    # Создаем список кортежей с данными и таблицей курсов обмена
    data_chunks_with_exchange = [(chunk, exchange_csv) for chunk in reader]

    # Используем пул процессов для обработки данных параллельно
    with ProcessPoolExecutor() as executor:
        processed_chunks = list(executor.map(process_data_chunk, data_chunks_with_exchange))

    # Объединяем обработанные части данных в один DataFrame
    df = pd.concat(processed_chunks, ignore_index=True)

    # Группируем данные по годам и вычисляем среднюю зарплату
    return df.groupby('year')['converted_salary'].mean().round()


def save_html_table(yearly_salaries, output_dir):
    # Преобразуем данные в DataFrame и задаем заголовок на русском
    yearly_salaries_df = yearly_salaries.reset_index()
    yearly_salaries_df.columns = ['Год', 'Средняя зарплата']

    # Преобразуем данные в HTML таблицу
    html_table = yearly_salaries_df.to_html(
        index=False,
        border=1,
        table_id='salary_table',
        classes='table table-dark'
    )

    # Добавляем CSS для кастомного дизайна таблицы
    style = """
    <style>
        #salary_table {
            background-color: #7766cf; /* цвет "sky purple" */
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
    html_path = os.path.join(output_dir, 'salary_by_year.html')

    # Создание папки, если она не существует
    os.makedirs(os.path.dirname(html_path), exist_ok=True)

    # Сохранение таблицы в HTML файл
    with open(html_path, 'w', encoding='utf-8-sig') as f:
        f.write(html_table)


def plot_yearly_salaries(yearly_salaries, img_dir):
    # Строим график по данным о средней зарплате за год
    plt.figure(figsize=(14, 10), facecolor='none')

    # График с вертикальными столбцами
    plt.bar(yearly_salaries.index.astype(str), yearly_salaries.values, label='Средняя зарплата', color='#9b59b6')

    # Заголовок и метки с черным цветом текста
    plt.title('Уровень зарплаты по годам', fontsize=20, color='black')
    plt.xlabel('Годы', fontsize=14, color='black')
    plt.ylabel('Средняя зарплата', fontsize=14, color='black')

    # Настройка меток осей и легенды с черным цветом текста
    plt.xticks(fontsize=12, color='black', rotation=45)
    plt.yticks(fontsize=12, color='black')
    plt.legend(fontsize=14, facecolor='none', edgecolor='black', loc='upper right')

    # Сетка
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    plt.tight_layout()

    # Сохранение изображения с прозрачным фоном
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    img_path = os.path.join(img_dir, 'salary_years_plot.png')
    plt.savefig(img_path, transparent=True, bbox_inches='tight')
    plt.close()


def main():
    # Пути к файлам данных
    file_path = '../../../data/vacancies_2024.csv'
    exchange_file_path = '../../../data/currency.csv'
    output_data_dir = 'data'
    img_dir = 'data/img'

    # Обработка данных и вычисление средней зарплаты по годам
    yearly_salaries = process_salary_data(file_path, exchange_file_path)

    # Сохранение таблицы в HTML файл
    save_html_table(yearly_salaries, output_data_dir)

    # Построение графика
    plot_yearly_salaries(yearly_salaries, img_dir)


if __name__ == '__main__':
    # Для работы с multiprocessing на Windows
    multiprocessing.freeze_support()
    main()
