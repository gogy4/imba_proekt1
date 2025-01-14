from django.shortcuts import render

# Рендеринг главной страницы
def home(request):
    return render(request, 'pages/home.html')
