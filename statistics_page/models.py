from django.db import models

class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.TextField()
    company = models.CharField(max_length=255)
    salary_from = models.FloatField(null=True, blank=True)
    salary_to = models.FloatField(null=True, blank=True)
    salary_currency = models.CharField(max_length=10, null=True, blank=True)
    region = models.CharField(max_length=255)
    publication_date = models.DateField()

    def __str__(self):
        return self.title
