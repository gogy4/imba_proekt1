from django.urls import path
from . import views

app_name = 'statistics_page'

urlpatterns = [
    path('/statistics_page/', views.statistics_page, name='statistics_page'),
]