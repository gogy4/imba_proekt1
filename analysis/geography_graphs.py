import os
import pandas as pd
import matplotlib.pyplot as plt


def make_salary_plot(salary_data: pd.DataFrame, name: str, name_plot: str):
    # Проверка и создание папки, если не существует
    output_dir = 'static_dev/geography/img'
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(salary_data['area_name'], salary_data['average_salary'], marker='o', label='Average Salary', color='green')
    plt.title(name_plot, color='white')
    plt.xlabel('Город', color='white')
    plt.ylabel('Средняя зарплата', color='white')
    plt.xticks(rotation=90, color='white')
    plt.yticks(color='white')
    plt.legend()
    plt.grid(True, color='white')
    plt.tight_layout()
    plt.gca().set_facecolor('#010409')  # Задание цвета фона графика
    plt.savefig(os.path.join(output_dir, name), transparent=True)
    plt.show()


def make_count_plot(vacancy_data: pd.DataFrame, name: str, name_plot: str):
    # Проверка и создание папки, если не существует
    output_dir = 'static_dev/geography/img'
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.pie(vacancy_data['vacancy_count'], labels=vacancy_data['area_name'], autopct='%1.1f%%', startangle=140,
            colors=['#4285f4', '#0f9d58', '#f4b400', '#db4437', '#34a853', '#735cff', '#ff6600'],
            textprops={'color': 'white'})  # Изменение цвета текста
    plt.title(name_plot, color='white')
    plt.axis('equal')
    plt.tight_layout()
    plt.gca().set_facecolor('#010409')  # Задание цвета фона графика
    plt.savefig(os.path.join(output_dir, name), transparent=True)
    plt.show()


def main():
    area_count_all = pd.read_csv('data/area_count_all.csv')
    area_count_prof = pd.read_csv('data/area_count_prof.csv')
    area_salary_all = pd.read_csv('data/area_salary_all.csv')
    area_salary_prof = pd.read_csv('data/area_salary_prof.csv')

    make_salary_plot(area_salary_all, name="area_salary_all_plot",
                     name_plot="Уровень зарплат по городам")
    make_salary_plot(area_salary_prof, name="area_salary_prof_plot",
                     name_plot="Уровень зарплат по городам для C/C++ программиста")
    make_count_plot(area_count_all, name="area_count_all_plot",
                    name_plot="Доля вакансий по городам")
    make_count_plot(area_count_prof, name="area_count_prof_plot",
                    name_plot="Доля вакансий по городам для C/C++ программиста")


if __name__ == "__main__":
    main()
