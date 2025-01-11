from django.db import models


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
