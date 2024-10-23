# RealEstatePriceForecast/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('property/', include('property.urls')),  # Użyj nazw aplikacji bez pełnej ścieżki
    path('user/', include('user.urls')),  # Przykładowe dodanie dla aplikacji 'user'
]