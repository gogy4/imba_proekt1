import pandas as pd
from collections import Counter
import os
import matplotlib.pyplot as plt


def create_skills_report(file_path):
    """
    Создание отчета по навыкам.
    """
    # Загрузка данных
    df = pd.read_csv(file_path, usecols=['key_skills'], encoding='utf-8-sig', low_memory=False)

    # Подсчет навыков
    skills_counter = Counter()

    # Обработка каждой строки
    for skills_str in df['key_skills']:
        if pd.isna(skills_str):
            continue
        skills = [skill.strip() for skill in str(skills_str).split('\n')]
        skills_counter.update(skills)

    # Получение топ-20 навыков
    top_skills = skills_counter.most_common(20)
    df_skills = pd.DataFrame(top_skills, columns=['Навык', 'Частота'])

    # Визуализация
    plot_skills(df_skills)

    return df_skills


def plot_skills(skills_df):
    """
    Визуализация топ-20 навыков и сохранение графика в папку static_dev/skills/img/.
    """
    # Убедимся, что папка static_dev/skills/img существует, если нет - создадим ее
    save_path = 'static_dev/skills/img'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Настройка темной темы matplotlib
    plt.style.use('dark_background')

    # Создание фигуры с прозрачным фоном
    plt.figure(figsize=(16, 10), facecolor='none')
    ax = plt.gca()
    ax.set_facecolor('none')

    # Фиолетовые оттенки для цветов
    colors = [
        '#8E44AD',  # Фиолетовый
        '#9B59B6',  # Лаванда
        '#6C3483',  # Темный фиолетовый
        '#AF7AC5',  # Светлый фиолетовый
        '#5B2C6F',  # Слива
        '#7D3C98',  # Яркий фиолетовый
        '#BB8FCE',  # Лавандовый
        '#884EA0',  # Пурпурный
        '#9B59B6',  # Сливовый
        '#76448A',  # Тёмный пурпурный
        '#D2B4DE',  # Легкий фиолетовый
        '#A569BD'   # Пастельный фиолетовый
    ]

    # Горизонтальный график
    bars = plt.barh(skills_df['Навык'], skills_df['Частота'], color=colors[:len(skills_df)])

    # Настройка графика
    plt.title('ТОП-20 навыков C/C++ программист', fontsize=24, color='black')  # Темный цвет заголовка
    plt.xlabel('Частота упоминаний', fontsize=14, color='black')  # Темный цвет для оси X
    plt.ylabel('Навык', fontsize=14, color='black')  # Темный цвет для оси Y

    # Цвета осей и тиков
    plt.tick_params(axis='x', colors='black')  # Темный цвет для оси X
    plt.tick_params(axis='y', colors='black')  # Темный цвет для оси Y

    # Сетка
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    plt.gca().invert_yaxis()  # Инвертируем ось Y для лучшей читаемости
    plt.tight_layout()

    # Сохранение с прозрачным фоном в папку static_dev/skills/img/
    file_path = os.path.join(save_path, 'skills_plot.png')
    plt.savefig(file_path, transparent=True, bbox_inches='tight')
    plt.close()  # Закрываем figure



def main():
    """
    Основная функция для создания отчета.
    """
    file_path = 'data/vacancies_by_name.csv'

    # Создание отчета
    create_skills_report(file_path)


if __name__ == "__main__":
    main()
