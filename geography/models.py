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