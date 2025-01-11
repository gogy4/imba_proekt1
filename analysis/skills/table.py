import pandas as pd
from collections import Counter
import os


def generate_skills_summary(file_path):
    """
    Генерация сводки по навыкам.
    """
    # Загрузка данных
    data = pd.read_csv(file_path, usecols=['key_skills'], encoding='utf-8-sig', low_memory=False)

    # Подсчет навыков
    skills_count = Counter()

    # Обработка каждой строки
    for skills_text in data['key_skills']:
        if pd.isna(skills_text):
            continue
        skills_list = [skill.strip() for skill in str(skills_text).split('\n')]
        skills_count.update(skills_list)

    # Получение топ-20 навыков
    top_skills_list = skills_count.most_common(20)
    skills_df = pd.DataFrame(top_skills_list, columns=['Навык', 'Частота'])

    # Сохранение в HTML
    save_skills_as_html(skills_df)

    return skills_df


def save_skills_as_html(skills_df):
    """
    Сохранение DataFrame с навыками в HTML-таблицу в папку data/ или в текущую папку.
    Путь сохранения: ./data/skills_report.html
    """
    # Путь к файлу
    file_path = os.path.join('data', 'skills_report.html')

    # Проверка, существует ли папка 'data'
    if not os.path.exists('data'):
        os.makedirs('data')  # Если нет, создаем

    # Сохранение HTML файла в папку data
    html_content = skills_df.to_html(index=False, border=1, classes='dataframe table table-dark', header=True)

    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.write(html_content)


def main():
    """
    Основная функция для генерации сводки.
    """
    file_path = 'data/vacancies_by_name.csv'

    # Генерация сводки
    generate_skills_summary(file_path)


if __name__ == "__main__":
    main()
