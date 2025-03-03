import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import matplotlib.pyplot as plt
import os


def process_chunk(data_chunk):
    # Обрабатываем кусок данных, вычисляя количество вакансий по каждому региону
    return data_chunk['area_name'].value_counts()


def calculate_area_shares(file_path):
    # Чтение данных и обработка с использованием нескольких потоков для подсчета доли вакансий по регионам
    data_reader = pd.read_csv(file_path, encoding='utf-8-sig', usecols=['area_name'], chunksize=500_000)

    with ProcessPoolExecutor() as executor:
        processed_data = list(executor.map(process_chunk, data_reader))

    # Объединяем все части данных и подсчитываем количество вакансий по каждому региону
    total_vacancies_by_area = pd.concat(processed_data).groupby(level=0).sum()
    total_vacancies = total_vacancies_by_area.sum()

    # Вычисляем долю вакансий для каждого региона
    area_shares = total_vacancies_by_area / total_vacancies
    # Отбираем топ-10 регионов с долей более 1%
    top_areas = area_shares[area_shares > 0.01].nlargest(10)

    # Добавляем долю для других регионов, которые не попали в топ-10
    top_areas['Другие'] = 1 - top_areas.sum()

    return top_areas


def save_area_shares_to_html(shares_df, output_folder):
    # Преобразуем данные в DataFrame и задаем заголовки на русском
    shares_df = shares_df.reset_index()
    shares_df.columns = ['Город', 'Доля вакансий']

    # Преобразуем данные в HTML таблицу
    html_table = shares_df.to_html(
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
    html_file_path = os.path.join(output_folder, 'vacancy_by_city.html')

    # Создание папки, если она не существует
    os.makedirs(os.path.dirname(html_file_path), exist_ok=True)

    # Сохранение таблицы в HTML файл
    with open(html_file_path, 'w', encoding='utf-8-sig') as file:
        file.write(html_table)


def create_area_shares_bar_chart(areas, shares, output_folder):
    # Создание графика с долей вакансий по регионам
    os.makedirs(output_folder, exist_ok=True)

    plt.style.use('ggplot')

    fig, ax = plt.subplots(figsize=(12, 8), facecolor='none')

    # Используем различные цвета для столбцов графика
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

    # Строим график с вертикальными столбцами для доли вакансий по регионам
    ax.bar(areas, shares, color=colors[:len(areas)])

    # Настройка заголовка и подписей осей с черным цветом
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

    # Настройка отступов для улучшения отображения
    plt.tight_layout()

    # Сохраняем график в файл
    image_path = os.path.join(output_folder, 'vacancy_by_city.png')
    plt.savefig(image_path, transparent=True)
    plt.close()


def main():
    # Путь к исходным данным о вакансиях
    file_path = '../../../data/vacancies_2024.csv'

    # Папки для сохранения изображений и HTML
    image_output_folder = 'data/img'
    html_output_folder = 'data'

    # Вычисление доли вакансий по регионам
    area_shares = calculate_area_shares(file_path)

    # Сохранение таблицы с данными в HTML
    save_area_shares_to_html(area_shares, html_output_folder)

    # Создание графика с долей вакансий по регионам
    create_area_shares_bar_chart(area_shares.index, area_shares.values, image_output_folder)


if __name__ == '__main__':
    # Для работы с multiprocessing на Windows
    multiprocessing.freeze_support()
    main()
