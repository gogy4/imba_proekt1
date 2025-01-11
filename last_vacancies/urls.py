from django.urls import path
from . import views

app_name = 'last_vacancies'

urlpatterns = [
    path('/last_vacancies/', views.last_vacancies, name='last_vacancies'),
]