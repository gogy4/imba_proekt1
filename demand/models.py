from django.db import models

class Demand(models.Model):
    salary_by_year_plot = models.ImageField(blank=False, verbose_name='График зарплат по годам (C/C++ программист)')
    salary_by_year_table = models.TextField(blank=False, verbose_name='Таблица зарплат по годам (C/C++ программист)')

    vacancy_by_year_plot = models.ImageField(blank=False, verbose_name='График количества вакансий по годам (C/C++ программист)')
    vacancy_by_year_table = models.TextField(blank=False, verbose_name='Таблица количества вакансий по годам (C/C++ программист)')

    class Meta:
        verbose_name = 'Востребованность вакансий'
