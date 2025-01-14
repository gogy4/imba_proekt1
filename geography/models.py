from django.db import models


class AreaSalaryAll(models.Model):
    area_name = models.CharField(max_length=255)
    average_salary = models.IntegerField()


class AreaCountAll(models.Model):
    area_name = models.CharField(max_length=255)
    vacancy_count = models.DecimalField(max_digits=5, decimal_places=2)


class AreaSalaryProf(models.Model):
    area_name = models.CharField(max_length=255)
    average_salary = models.IntegerField()


class AreaCountProf(models.Model):
    area_name = models.CharField(max_length=255)
    vacancy_count = models.DecimalField(max_digits=5, decimal_places=2)

class Geography(models.Model):
    salary_by_city_plot = models.ImageField(blank=False, verbose_name='График зарплат по городам (C/C++ программист)')
    salary_by_city_table = models.TextField(blank=False, verbose_name='Таблица зарплат по городам (C/C++ программист)')

    vacancy_by_city_plot = models.ImageField(blank=False, verbose_name='График долей вакансий по городам (C/C++ программист)')
    vacancy_by_city_table = models.TextField(blank=False, verbose_name='Таблица доли вакансий по городам (C/C++ программист)')

    class Meta:
        verbose_name = 'География вакансий'