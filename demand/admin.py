from django.contrib import admin
from .models import *

# Регистрация модели Demand в административной панели
admin.site.register(Demand)
