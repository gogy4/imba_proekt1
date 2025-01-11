# Generated by Django 5.1.4 on 2024-12-30 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicCountAll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('vacancy_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DynamicCountProf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('vacancy_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DynamicSalaryAll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('average_salary', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DynamicSalaryProf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('average_salary', models.IntegerField()),
            ],
        ),
    ]
