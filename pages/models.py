from django.db import models


class DynamicSalaryAll(models.Model):
    year = models.IntegerField()
    average_salary = models.IntegerField()


class DynamicCountAll(models.Model):
    year = models.IntegerField()
    vacancy_count = models.IntegerField()


class DynamicSalaryProf(models.Model):
    year = models.IntegerField()
    average_salary = models.IntegerField()


class DynamicCountProf(models.Model):
    year = models.IntegerField()
    vacancy_count = models.IntegerField()