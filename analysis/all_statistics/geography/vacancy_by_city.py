import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import matplotlib.pyplot as plt
import os


def process_chunk(data_chunk):
    return data_chunk['area_name'].value_counts()


def calculate_area_shares(file_path):
    data_reader = pd.read_csv(file_path, encoding='utf-8-sig', usecols=['area_name'], chunksize=500_000)

    with ProcessPoolExecutor() as executor:
        processed_data = list(executor.map(process_chunk, data_reader))

    total_vacancies_by_area = pd.concat(processed_data).groupby(level=0).sum()
    total_vacancies = total_vacancies_by_area.sum()

    area_shares = total_vacancies_by_area / total_vacancies
    top_areas = area_shares[area_shares > 0.01].nlargest(10)

    top_areas['Другие'] = 1 - top_areas.sum()

    return top_areas


def save_area_shares_to_html(shares_df, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    shares_df = shares_df.reset_index()
    shares_df.columns = ['Город', 'Доля вакансий']

    html_content = shares_df.to_html(
        index=False, border=1, classes='dataframe table table-dark', float_format='{:.1%}'.format)

    html_content = html_content.replace('<table', '<table style="width: 60%; margin-left: auto; margin-right: auto; border-collapse: collapse;"')
    html_content = html_content.replace('<td>', '<td style="text-align: center;">')
    html_content = html_content.replace('<th>', '<th style="text-align: center;">')

    html_path = os.path.join(output_folder, 'vacancy_by_city.html')

    with open(html_path, 'w', encoding='utf-8-sig') as file:
        file.write(html_content)


def create_area_shares_bar_chart(areas, shares, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    plt.style.use('ggplot')

    fig, ax = plt.subplots(figsize=(12, 8), facecolor='none')

    # Используем цвета для столбцов
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
        '#0000CD'  # Темно-синий
    ]

    ax.bar(areas, shares, color=colors[:len(areas)])

    # Заголовок и подписи осей с черным цветом
    ax.set_title('Доля вакансий по регионам', fontsize=24, color='black')
    ax.set_xlabel('Город', fontsize=16, color='black')
    ax.set_ylabel('Доля вакансий', fontsize=16, color='black')

    # Поворачиваем метки на оси X для лучшего восприятия
    plt.xticks(rotation=45, ha='right', color='black')
    plt.yticks(color='black')

    # Настройка цвета текста для меток на столбцах
    for label in ax.get_xticklabels():
        label.set_color('black')

    for label in ax.get_yticklabels():
        label.set_color('black')

    plt.tight_layout()

    image_path = os.path.join(output_folder, 'vacancy_by_city.png')
    plt.savefig(image_path, transparent=True)
    plt.close()


def main():
    file_path = '../../../data/vacancies_2024.csv'

    image_output_folder = 'data/img'
    html_output_folder = 'data'

    area_shares = calculate_area_shares(file_path)
    save_area_shares_to_html(area_shares, html_output_folder)
    create_area_shares_bar_chart(area_shares.index, area_shares.values, image_output_folder)



if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
