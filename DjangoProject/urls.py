from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Путь к административной панели
    path('admin/', admin.site.urls),

    # Путь к главной странице (home)
    path('', include('home.urls')),

    # Путь к странице статистики
    path('statistics_page/', include('statistics_page.urls')),

    # Путь к странице с данными о спросе
    path('demand/', include('demand.urls')),

    # Путь к странице географической информации
    path('geography/', include('geography.urls')),

    # Путь к странице с навыками
    path('skills/', include('skills.urls')),

    # Путь к странице с последними вакансиями
    path('last_vacancies/', include('last_vacancies.urls')),
]

# Если в настройках включен режим отладки, добавляем путь для медиафайлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
