from django.db import models


class Demand(models.Model):
    # Поле для изображения графика зарплат по годам
    salary_by_year_plot = models.ImageField(blank=False, verbose_name='График зарплат по годам (C/C++ программист)')

    # Поле для текста таблицы зарплат по годам
    salary_by_year_table = models.TextField(blank=False, verbose_name='Таблица зарплат по годам (C/C++ программист)')

    # Поле для изображения графика количества вакансий по годам
    vacancy_by_year_plot = models.ImageField(blank=False,
                                             verbose_name='График количества вакансий по годам (C/C++ программист)')

    # Поле для текста таблицы количества вакансий по годам
    vacancy_by_year_table = models.TextField(blank=False,
                                             verbose_name='Таблица количества вакансий по годам (C/C++ программист)')

    class Meta:
        # Настройка отображаемого имени модели
        verbose_name = 'Востребованность вакансий'
