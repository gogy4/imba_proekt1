from django.shortcuts import render
from .models import Home

def home(request):
    # Попытка найти первую запись в модели Home
    stat = Home.objects.first()

    # Если запись не найдена
    if stat is None:
        return render(request, 'pages/home.html', {'error': 'Нет данных'})

    # Создание контекста для рендеринга шаблона
    context = {
        'c_plot': stat.c_plot.url if stat.c_plot else None,
        'cplusplus_plot': stat.cplusplus_plot.url if stat.cplusplus_plot else None,  # Исправлено на латинскую "c"
        'prof': 'C/C++ программист',
    }

    # Рендеринг страницы с данными
    return render(request, 'pages/home.html', context)
