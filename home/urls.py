from django.urls import path
from . import views

# Указываем имя приложения
app_name = 'home'

urlpatterns = [
    # Путь к главной странице
    path('', views.home, name='home'),
]
