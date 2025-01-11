import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_vacancy_distribution(cities, shares):
    # Устанавливаем стиль ggplot
    plt.style.use('ggplot')

    # Создание фигуры с заданным размером
    plt.figure(figsize=(12, 8), facecolor='none')
    ax = plt.gca()
    ax.set_facecolor('none')

    # Один фиксированный цвет для всех частей графика
    single_color = '#3498DB'  # Насыщенный синий

    # График доли вакансий по городам
    plt.pie(shares, labels=cities, autopct='%1.1f%%',
            textprops={'fontsize': 10, 'color': 'black'},  # Цвет текста поменяли на черный для лучшего контраста
            colors=[single_color] * len(cities))  # Все части графика одного цвета

    plt.title('Доля вакансий по городам C/C++ программист', fontsize=24, color='black')

    # Создание папки, если ее нет
    if not os.path.exists('static_dev/geography/img'):
        os.makedirs('static_dev/geography/img')

    # Сохранение графика в файл
    plt.tight_layout()
    plt.savefig('static_dev/geography/img/vacancy_distribution.png')
    plt.close()

def plot_average_salaries(salary_data):
    # Сортировка данных для визуализации по убыванию
    sorted_salaries = salary_data.sort_values(ascending=False)

    plt.style.use('ggplot')
    plt.figure(figsize=(12, 8), facecolor='none')
    ax = plt.gca()
    ax.set_facecolor('none')

    colors = plt.get_cmap('viridis')(np.linspace(0, 1, len(sorted_salaries)))
    plt.barh(sorted_salaries.index, sorted_salaries.values, color=colors)

    # Инвертируем ось Y, чтобы самое большое значение было сверху
    plt.gca().invert_yaxis()

    plt.title('Средняя зарплата по городам C/C++ программист', fontsize=20)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.xlabel('Средняя зарплата (руб.)')
    plt.tight_layout()

    # Сохранение графика в файл
    plt.savefig('static_dev/geography/img/average_salaries.png')
    plt.close()

def main():
    # Пример данных для демонстрации
    city_names = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань', 'Другие']
    vacancy_shares = [0.4, 0.2, 0.15, 0.1, 0.1, 0.05]

    city_list = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань']
    salary_values = [120000, 110000, 95000, 90000, 85000]

    salary_data = pd.Series(salary_values, index=city_list)

    # Построение и сохранение графиков
    plot_vacancy_distribution(city_names, vacancy_shares)
    plot_average_salaries(salary_data)

if __name__ == '__main__':
    main()
