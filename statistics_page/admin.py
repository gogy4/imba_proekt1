from django.contrib import admin
from .models import StatisticsPage

# Класс для настройки отображения модели в админке
class StatisticsPageAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке объектов на странице админки
    list_display = [
        'salary_by_year_plot', 'salary_by_year_table',
        'vacancies_by_year_plot', 'vacancies_by_year_table',
        'salary_by_city_plot', 'salary_by_city_table',
        'vacancy_share_by_city_plot', 'vacancy_share_by_city_table',
        'top_skills_plot_2015', 'top_skills_table_2015',
        'top_skills_plot_2016', 'top_skills_table_2016',
        'top_skills_plot_2017', 'top_skills_table_2017',
        'top_skills_plot_2018', 'top_skills_table_2018',
        'top_skills_plot_2019', 'top_skills_table_2019',
        'top_skills_plot_2020', 'top_skills_table_2020',
        'top_skills_plot_2021', 'top_skills_table_2021',
        'top_skills_plot_2022', 'top_skills_table_2022',
        'top_skills_plot_2023', 'top_skills_table_2023',
        'top_skills_plot_2024', 'top_skills_table_2024',
    ]

    # Поля, по которым можно будет искать данные в админке
    search_fields = [
        'salary_by_year_plot', 'salary_by_year_table',
        'vacancies_by_year_plot', 'vacancies_by_year_table',
        'salary_by_city_plot', 'salary_by_city_table',
        'vacancy_share_by_city_plot', 'vacancy_share_by_city_table',
        'top_skills_plot_2015', 'top_skills_table_2015',
        'top_skills_plot_2016', 'top_skills_table_2016',
        'top_skills_plot_2017', 'top_skills_table_2017',
        'top_skills_plot_2018', 'top_skills_table_2018',
        'top_skills_plot_2019', 'top_skills_table_2019',
        'top_skills_plot_2020', 'top_skills_table_2020',
        'top_skills_plot_2021', 'top_skills_table_2021',
        'top_skills_plot_2022', 'top_skills_table_2022',
        'top_skills_plot_2023', 'top_skills_table_2023',
        'top_skills_plot_2024', 'top_skills_table_2024',
    ]

# Регистрируем модель StatisticsPage в админке с настройками из StatisticsPageAdmin
admin.site.register(StatisticsPage, StatisticsPageAdmin)
