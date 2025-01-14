import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def process_vacancy_chunk(vacancy_chunk):
    vacancy_chunk['year'] = pd.to_datetime(vacancy_chunk['published_at'], utc=True).dt.year
    return vacancy_chunk['year'].value_counts()


def process_file_years(file_path):
    reader = pd.read_csv(file_path, encoding='utf-8-sig', low_memory=False, usecols=['published_at'], chunksize=500_000)
    with ProcessPoolExecutor() as executor:
        processed_data = executor.map(process_vacancy_chunk, reader)

    return pd.concat(processed_data).groupby(level=0).sum().sort_index()


def save_to_html(vacancies_by_year):
    os.makedirs('data/', exist_ok=True)

    # Преобразуем данные в DataFrame
    vacancies_by_year_df = vacancies_by_year.reset_index()
    vacancies_by_year_df.columns = ['Год', 'Количество вакансий']

    # Преобразуем данные в HTML таблицу
    html_table = vacancies_by_year_df.to_html(
        index=False,
        border=1,
        table_id='vacancy_by_year_table',
        classes='table table-dark'
    )

    # Добавляем CSS для кастомного дизайна
    style = """
    <style>
        #vacancy_by_year_table {
            background-color: #7766cf; /* skypurple */
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 15px;
            overflow: hidden;
        }
        #vacancy_by_year_table th, #vacancy_by_year_table td {
            text-align: center;
            border: 1px solid #594f99;
            padding: 10px;
        }
        #vacancy_by_year_table th {
            background-color: #594f99;
            color: white;
        }
        #vacancy_by_year_table td {
            color: white;
        }
    </style>
    """

    # Добавляем CSS перед таблицей
    html_table = style + html_table

    # Путь для сохранения HTML файла
    html_file_path = 'data/vacancies_by_year.html'

    # Создание папки, если она не существует
    os.makedirs(os.path.dirname(html_file_path), exist_ok=True)

    # Сохранение таблицы в HTML файл
    with open(html_file_path, 'w', encoding='utf-8-sig') as file:
        file.write(html_table)



def create_yearly_plot(years, counts, img_dir='data/img/'):
    os.makedirs(img_dir, exist_ok=True)

    plt.style.use('dark_background')
    plt.figure(figsize=(12, 8), facecolor='none')

    bars = plt.bar(years, counts, color='#9b59b6')  # Set color to #9b59b6
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), int(bar.get_height()), ha='center', va='bottom',
                 color='black')  # Change text color to black

    # Set title, labels, and legend text color to black
    plt.title('Количество вакансий по годам', fontsize=16, color='black')
    plt.xlabel('Годы', fontsize=12, color='black')
    plt.ylabel('Количество вакансий', fontsize=12, color='black')

    # Set ticks color to black for both axes
    plt.xticks(color='black')
    plt.yticks(color='black')

    # Set grid lines and color for the y-axis
    plt.grid(True, axis='y', color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    # Ensure all other text is black as well
    for label in plt.gca().get_xticklabels():
        label.set_color('black')
    for label in plt.gca().get_yticklabels():
        label.set_color('black')

    # Ensure all text on the figure is black
    plt.tight_layout()

    # Save the plot
    plt.savefig(img_dir + 'vacancies_by_year.png', transparent=True)



def main():
    file_path = '../../../data/vacancies_2024.csv'
    vacancies_by_year = process_file_years(file_path)
    save_to_html(vacancies_by_year)
    create_yearly_plot(vacancies_by_year.index, vacancies_by_year.values)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
