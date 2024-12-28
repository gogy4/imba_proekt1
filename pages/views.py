from django.shortcuts import render


def home(request):
    return render(request, 'base.html')

def statistics(request):
    return render(request, 'base.html')

def demand(request):
    return render(request, 'base.html')

def geography(request):
    return render(request, 'base.html')

def skills(request):
    return render(request, 'base.html')

def last_vacancies(request):
    return render(request, 'base.html')