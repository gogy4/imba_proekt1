from django.db import models

# Модель для статистической страницы
class StatisticsPage(models.Model):
    # График и таблица зарплат по годам (Общая)
    salary_by_year_plot = models.ImageField(blank=True, null=True, verbose_name='График зарплат по годам (Общая)')
    salary_by_year_table = models.TextField(blank=True, null=True, verbose_name='Таблица зарплат по годам (Общая)')

    # График и таблица количества вакансий по годам (Общая)
    vacancies_by_year_plot = models.ImageField(blank=True, null=True, verbose_name='График количества вакансий по годам (Общая)')
    vacancies_by_year_table = models.TextField(blank=True, null=True, verbose_name='Таблица количества вакансий по годам (Общая)')

    # График и таблица зарплат по городам (Общая)
    salary_by_city_plot = models.ImageField(blank=True, null=True, verbose_name='График зарплат по городам (Общая)')
    salary_by_city_table = models.TextField(blank=True, null=True, verbose_name='Таблица зарплат по городам (Общая)')

    # График и таблица долей вакансий по городам (Общая)
    vacancy_share_by_city_plot = models.ImageField(blank=True, null=True, verbose_name='График долей вакансий по городам (Общая)')
    vacancy_share_by_city_table = models.TextField(blank=True, null=True, verbose_name='Таблица доли вакансий по городам (Общая)')

    # Графики и таблицы топ-20 навыков по годам (Общая)
    top_skills_plot_2015 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2015 (Общая)')
    top_skills_table_2015 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2015 (Общая)')

    top_skills_plot_2016 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2016 (Общая)')
    top_skills_table_2016 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2016 (Общая)')

    top_skills_plot_2017 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2017 (Общая)')
    top_skills_table_2017 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2017 (Общая)')

    top_skills_plot_2018 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2018 (Общая)')
    top_skills_table_2018 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2018 (Общая)')

    top_skills_plot_2019 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2019 (Общая)')
    top_skills_table_2019 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2019 (Общая)')

    top_skills_plot_2020 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2020 (Общая)')
    top_skills_table_2020 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2020 (Общая)')

    top_skills_plot_2021 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2021 (Общая)')
    top_skills_table_2021 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2021 (Общая)')

    top_skills_plot_2022 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2022 (Общая)')
    top_skills_table_2022 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2022 (Общая)')

    top_skills_plot_2023 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2023 (Общая)')
    top_skills_table_2023 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2023 (Общая)')

    top_skills_plot_2024 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2024 (Общая)')
    top_skills_table_2024 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2024 (Общая)')

    class Meta:
        verbose_name = 'Статистика по трудоустройству'
