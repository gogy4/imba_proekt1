from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('/statistics/', views.statistics, name='statistics'),
    path('/demand/', views.demand, name='demand'),
    path('/geography/', views.geography, name='geography'),
    path('/skills/', views.skills, name='skills'),
    path('/last_vacancies/', views.last_vacancies, name='last_vacancies'),
]