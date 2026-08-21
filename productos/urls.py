from django.urls import path

from . import views


urlpatterns = [
    path('', views.productos, name='productos'),
    path('api/', views.lista_productos, name='lista_productos'),
]