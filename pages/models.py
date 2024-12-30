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

class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.TextField()
    company = models.CharField(max_length=255)
    salary_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_to = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=4, null=True, blank=True)
    region = models.CharField(max_length=100)
    publication_date = models.DateTimeField()

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