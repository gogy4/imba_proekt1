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
    # Создаем папку, если не существует
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Создаем DataFrame и сохраняем в формате HTML
    df = pd.DataFrame(data, columns=['Навык', 'Количество'])
    html = df.to_html(index=False, border=1, classes='table table-dark', header=True)
    html = html.replace('<table',
                        f'<table style="width: 60%; margin-left: auto; margin-right: auto; border-collapse: collapse;"')
    html = html.replace('<td>', '<td style="text-align: center; width: 33.33%;">')
    html = html.replace('<th>', '<th style="text-align: center; width: 33.33%;">')

    with open(filename, 'w', encoding='utf-8-sig') as f:
        f.write(html)


def extract_all_skills(df: pd.DataFrame, year=None) -> list:
    # Фильтруем данные по году, если необходимо
    if year is not None:
        df = df[df['year'] == year]

    # Извлекаем все навыки и приводим их к единому формату
    skills = df['key_skills'].str.split("\n").explode().dropna().tolist()
    return skills


def execute():
    # Путь к файлу данных
    vacancies_path = '../../../data/vacancies_2024.csv'

    # Чтение файла с указанием dtype для столбца key_skills (например, как строка)
    # В этом случае мы избегаем смешанных типов в этом столбце
    df = pd.read_csv(vacancies_path, dtype={"key_skills": str}, low_memory=False)

    # Продолжение работы с данными
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True)
    df['year'] = df['published_at'].dt.year

    # Период времени, который нас интересует
    unique_years = list(range(2015, 2025))

    for year in unique_years:
        # Извлекаем все навыки за год
        skills_all = extract_all_skills(df, year)

        # Извлекаем топ-20 навыков
        skills_all_top = extract_top_skills(skills_all)

        # Сохраняем результаты в HTML
        save_to_html(year, skills_all_top, f'data/top_skill_by_{year}.html')

        # Строим график
        data_year = pd.DataFrame(skills_all_top, columns=['Навык', 'Количество'])
        create_bar_chart(data_year, f'Топ 20 Навыков за {year} год', 'Количество', 'Навыки',
                         f'data/img/top_skill_by_{year}.png')


if __name__ == "__main__":
    execute()
