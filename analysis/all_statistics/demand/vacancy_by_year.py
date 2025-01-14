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

    vacancies_by_year_df = vacancies_by_year.reset_index()
    vacancies_by_year_df.columns = ['Год', 'Количество вакансий']

    html = vacancies_by_year_df.to_html(index=False, border=1, classes='table table-dark', header=True)

    html = html.replace('<table',
                        '<table style="width: 60%; margin-left: auto; margin-right: auto; border-collapse: collapse;"')

    html = html.replace('<td>', '<td style="text-align: center;">')
    html = html.replace('<th>', '<th style="text-align: center;">')

    with open('data/vacancies_by_year.html', 'w', encoding='utf-8-sig') as f:
        f.write(html)


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

    # Set legend text color to black
    plt.legend(['Количество вакансий'], fontsize=10, facecolor='none', edgecolor='white', loc='upper right',
               frameon=False, labelcolor='black', textcolor='black')

    # Set grid lines and color for the y-axis
    plt.grid(True, axis='y', color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    # Ensure all other text is black as well
    for label in plt.gca().get_xticklabels():
        label.set_color('black')
    for label in plt.gca().get_yticklabels():
        label.set_color('black')
    for label in plt.gca().get_legend().get_texts():
        label.set_color('black')

    # Ensure all text on the figure is black
    plt.tight_layout()
    img_path = os.path.join(img_dir, 'vacancies_by_year_vertical.png')
    plt.savefig(img_path, transparent=True)


def main():
    file_path = '../../../data/vacancies_2024.csv'
    vacancies_by_year = process_file_years(file_path)
    save_to_html(vacancies_by_year)
    create_yearly_plot(vacancies_by_year.index, vacancies_by_year.values)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
