from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),        # Página de portada
    path('calculadora/', views.index, name='index'),  # Calculadora
]
