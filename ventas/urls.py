from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ventas, name='lista_ventas'),
]