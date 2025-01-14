from django.urls import path
from . import views

# Указываем имя приложения
app_name = 'skills'

urlpatterns = [
    # Путь к странице с навыками
    path('skills/', views.skills, name='skills'),
]
