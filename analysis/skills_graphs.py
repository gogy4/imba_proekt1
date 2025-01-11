import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_bar_chart(data, title, xlabel, ylabel, filename):
    # Создаем папку, если её нет
    output_dir = os.path.dirname(filename)
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.bar(data['skill_name'], data['count'], color='#4285f4')  # Цвет столбцов
    plt.title(title, color='white')  # Цвет заголовка
    plt.xlabel(xlabel, color='white')  # Цвет подписей осей x и y
    plt.ylabel(ylabel, color='white')
    plt.xticks(rotation=45, ha='right', color='white')  # Цвет текста на оси x
    plt.yticks(color='white')  # Цвет текста на оси y
    plt.gca().spines['bottom'].set_color('white')  # Цвет оси x
    plt.gca().spines['top'].set_color('white')
    plt.gca().spines['right'].set_color('white')
    plt.gca().spines['left'].set_color('white')
    plt.grid(True, color='white')  # Цвет сетки
    plt.tight_layout()
    plt.gca().set_facecolor('#010409')  # Задание цвета фона графика
    plt.savefig(filename, transparent=True)
    plt.show()


def main():
    skills_all_top = pd.read_csv('data/top_skills_all.csv')
    skills_prof_top = pd.read_csv('data/top_skills_prof.csv')

    unique_years = list(range(2017, 2024))
    for year in unique_years:
        plot_bar_chart(
            skills_all_top[skills_all_top['year'] == year][['skill_name', 'count']],
            f'Топ 20 Навыков за {year} год',
            'Навыки', 'Количество',
            f'static_dev/skills/img/bar_chart_all_{year}.png'
        )

        plot_bar_chart(
            skills_prof_top[skills_prof_top['year'] == year][['skill_name', 'count']],
            f'Топ 20 Навыков за {year} год для С++ Разработчика',
            'Навыки', 'Количество',
            f'static_dev/skills/img/bar_chart_prof_{year}.png'
        )


if __name__ == "__main__":
    main()
