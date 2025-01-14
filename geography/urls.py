from django.urls import path
from . import views

# Указываем имя приложения
app_name = 'geography'

urlpatterns = [
    # Путь к странице с географической информацией
    path('/geography/', views.geography, name='geography'),
]
