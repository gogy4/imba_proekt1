from django.db import models

class AreaSalaryAll(models.Model):
    # Название области
    area_name = models.CharField(max_length=255)
    # Средняя зарплата в области
    average_salary = models.IntegerField()


class AreaCountAll(models.Model):
    # Название области
    area_name = models.CharField(max_length=255)
    # Количество вакансий в области
    vacancy_count = models.DecimalField(max_digits=5, decimal_places=2)


class AreaSalaryProf(models.Model):
    # Название области
    area_name = models.CharField(max_length=255)
    # Средняя зарплата для профессии в области
    average_salary = models.IntegerField()


class AreaCountProf(models.Model):
    # Название области
    area_name = models.CharField(max_length=255)
    # Количество вакансий для профессии в области
    vacancy_count = models.DecimalField(max_digits=5, decimal_places=2)

class Geography(models.Model):
    # График зарплат по городам
    salary_by_city_plot = models.ImageField(blank=False, verbose_name='График зарплат по городам (C/C++ программист)')
    # Таблица зарплат по городам
    salary_by_city_table = models.TextField(blank=False, verbose_name='Таблица зарплат по городам (C/C++ программист)')

    # График долей вакансий по городам
    vacancy_by_city_plot = models.ImageField(blank=False, verbose_name='График долей вакансий по городам (C/C++ программист)')
    # Таблица доли вакансий по городам
    vacancy_by_city_table = models.TextField(blank=False, verbose_name='Таблица доли вакансий по городам (C/C++ программист)')

    class Meta:
        # Настройка отображаемого имени модели
        verbose_name = 'География вакансий'
