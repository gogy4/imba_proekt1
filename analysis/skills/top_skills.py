import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os


def extract_top_skills(all_skills: list) -> list:
    # Используем Counter напрямую для получения наиболее частых навыков
    return Counter(all_skills).most_common(20)


def create_bar_chart(data, title, xlabel, ylabel, filename):
    # Создаем папку для сохранения изображения, если она не существует
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Построение горизонтального барчарта
    plt.figure(figsize=(10, 6))
    plt.barh(data['Навык'], data['Количество'], color='#9b59b6')

    # Добавляем заголовки и метки
    plt.title(title, color='black')
    plt.xlabel(xlabel, color='black')
    plt.ylabel(ylabel, color='black')

    # Настройка осей
    plt.xticks(color='black')
    plt.yticks(color='black')
    plt.gca().spines['bottom'].set_color('black')
    plt.gca().spines['top'].set_color('black')
    plt.gca().spines['right'].set_color('black')
    plt.gca().spines['left'].set_color('black')

    # Добавление сетки и настройка внешнего вида
    plt.grid(True, color='black', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Устанавливаем цвет фона на темный
    plt.gca().set_facecolor('#010409')

    # Сохраняем изображение
    plt.savefig(filename, transparent=True)


def save_to_html(year: int, data: list, filename: str):
    # Преобразуем данные в DataFrame
    df = pd.DataFrame(data, columns=['Навык', 'Количество'])

    # Преобразуем данные в HTML таблицу
    html_table = df.to_html(
        index=False,
        border=1,
        table_id='skill_table',
        classes='table table-dark'
    )

    # Добавляем CSS для кастомного дизайна
    style = """
    <style>
        #skill_table {
            background-color: #7766cf; /* skypurple */
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 15px;
            overflow: hidden;
        }
        #skill_table th, #skill_table td {
            text-align: center;
            border: 1px solid #594f99;
            padding: 10px;
        }
        #skill_table th {
            background-color: #594f99;
            color: white;
        }
        #skill_table td {
            color: white;
        }
    </style>
    """

    # Добавляем CSS перед таблицей
    html_table = style + html_table

    # Создаем папку, если она не существует
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Сохраняем таблицу в HTML файл
    with open(filename, 'w', encoding='utf-8-sig') as file:
        file.write(html_table)



def extract_all_skills(df: pd.DataFrame, year=None) -> list:
    # Фильтруем данные по году, если необходимо
    if year is not None:
        df = df[df['year'] == year]

    # Извлекаем все навыки и приводим их к единому формату
    skills = df['key_skills'].str.split("\n").explode().dropna().tolist()
    return skills


def execute():
    # Путь к файлу данных о вакансиях
    vacancies_path = '../../data/vacancies_by_name.csv'

    # Чтение данных из CSV-файла
    # Мы указываем, что столбец 'key_skills' нужно интерпретировать как строку (dtype={"key_skills": str}),
    # чтобы избежать ошибок, связанных со смешанными типами данных.
    # low_memory=False используется для предотвращения предупреждений при чтении больших файлов.
    df = pd.read_csv(vacancies_path, dtype={"key_skills": str}, low_memory=False)

    # Преобразуем столбец 'published_at' в формат даты и времени с указанием часового пояса UTC.
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True)

    # Извлекаем год из даты публикации вакансии и сохраняем его в отдельный столбец 'year'.
    df['year'] = df['published_at'].dt.year

    # Определяем список уникальных годов, которые нас интересуют (с 2015 по 2024 включительно).
    unique_years = list(range(2015, 2025))

    # Цикл для обработки данных по каждому году
    for year in unique_years:
        # Извлекаем все навыки, указанные в вакансиях за определённый год.
        # Функция `extract_all_skills` должна возвращать словарь или другой объект с данными о навыках и их частоте.
        skills_all = extract_all_skills(df, year)

        # Извлекаем топ-20 самых популярных навыков за год.
        # Функция `extract_top_skills` сортирует навыки по частоте и возвращает топ-20.
        skills_all_top = extract_top_skills(skills_all)

        # Сохраняем результаты анализа в HTML-файл.
        # Например, таблицу с топ-20 навыками.
        save_to_html(year, skills_all_top, f'data/top_skill_by_{year}.html')

        # Строим столбчатую диаграмму по данным топ-20 навыков.
        # Сначала преобразуем данные в DataFrame для удобства работы с графиком.
        data_year = pd.DataFrame(skills_all_top, columns=['Навык', 'Количество'])

        # Создаём график с заголовком, где указывается год,
        # и сохраняем его как PNG-изображение.
        create_bar_chart(
            data_year,  # Данные для построения графика
            f'Топ 20 Навыков за {year} год',  # Заголовок графика
            'Количество',  # Подпись оси Y
            'Навыки',  # Подпись оси X
            f'data/img/top_skill_by_{year}.png'  # Путь для сохранения изображения
        )


# Если этот файл запускается как основная программа, вызываем функцию execute.
if __name__ == "__main__":
    execute()
