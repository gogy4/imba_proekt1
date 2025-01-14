from django.db import models

class Skills(models.Model):
    # Графики и таблицы для топ-20 навыков по годам с 2015 по 2024 для профессии C/C++ программист

    top_skills_plot_2015 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2015 (C/C++ программист)')
    top_skills_table_2015 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2015 (C/C++ программист)')

    top_skills_plot_2016 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2016 (C/C++ программист)')
    top_skills_table_2016 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2016 (C/C++ программист)')

    top_skills_plot_2017 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2017 (C/C++ программист)')
    top_skills_table_2017 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2017 (C/C++ программист)')

    top_skills_plot_2018 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2018 (C/C++ программист)')
    top_skills_table_2018 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2018 (C/C++ программист)')

    top_skills_plot_2019 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2019 (C/C++ программист)')
    top_skills_table_2019 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2019 (C/C++ программист)')

    top_skills_plot_2020 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2020 (C/C++ программист)')
    top_skills_table_2020 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2020 (C/C++ программист)')

    top_skills_plot_2021 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2021 (C/C++ программист)')
    top_skills_table_2021 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2021 (C/C++ программист)')

    top_skills_plot_2022 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2022 (C/C++ программист)')
    top_skills_table_2022 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2022 (C/C++ программист)')

    top_skills_plot_2023 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2023 (C/C++ программист)')
    top_skills_table_2023 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2023 (C/C++ программист)')

    top_skills_plot_2024 = models.ImageField(blank=True, null=True, verbose_name='График топ-20 навыков 2024 (C/C++ программист)')
    top_skills_table_2024 = models.TextField(blank=True, null=True, verbose_name='Таблица топ-20 навыков 2024 (C/C++ программист)')

    class Meta:
        verbose_name = 'Топ-20 навыков'
