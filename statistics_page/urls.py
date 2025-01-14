from django.urls import path
from . import views

# Устанавливаем имя приложения для маршрутов
app_name = 'statistics_page'

# Список URL-маршрутов для приложения statistics_page
urlpatterns = [
    # Маршрут для страницы статистики
    path('/statistics_page/', views.statistics_page, name='statistics_page'),
]
