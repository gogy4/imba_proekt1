from django.urls import path
from . import views

# Указываем имя приложения
app_name = 'last_vacancies'

urlpatterns = [
    # Путь к странице с последними вакансиями
    path('/last_vacancies/', views.last_vacancies, name='last_vacancies'),
]
