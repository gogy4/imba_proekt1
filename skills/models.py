from django.db import models


class TopSkillsAll(models.Model):
    skill_name = models.CharField(max_length=255)
    count = models.IntegerField()
    year = models.IntegerField()


class TopSkillsProf(models.Model):
    skill_name = models.CharField(max_length=255)
    count = models.IntegerField()
    year = models.IntegerField()