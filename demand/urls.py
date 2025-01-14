from django.urls import path
from . import views

# Указываем имя приложения
app_name = 'demand'

urlpatterns = [
    # Маршрут для страницы с запросом данных о спросе
    path('/demand/', views.demand, name='demand'),
]
