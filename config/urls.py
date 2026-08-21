"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from productos import views
from clientes import views as clientes_views
from proveedores import views as proveedores_views
from movimientos import views as movimientos_views
from ventas import views as ventas_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('dashboard.urls')),

    path('productos/', views.productos, name='productos'),

    path(
        'productos/nuevo/',
        views.crear_producto,
        name='crear_producto'
    ),

    path(
       'productos/<int:producto_id>/editar/',
        views.editar_producto,
        name='editar_producto'
    ),


    path(
       'productos/<int:producto_id>/eliminar/',
        views.eliminar_producto,
        name='eliminar_producto'
    ),
     
    path('clientes/', clientes_views.clientes, name='clientes'),

    path(
       'clientes/nuevo/',
        clientes_views.crear_cliente,
        name='crear_cliente'
    ),

    path(
       'clientes/<int:cliente_id>/editar/',
        clientes_views.editar_cliente,
        name='editar_cliente'
    ),

    path(
       'clientes/<int:cliente_id>/eliminar/',
        clientes_views.eliminar_cliente,
        name='eliminar_cliente'
    ),

    path(
       'proveedores/',
        proveedores_views.proveedores,
        name='proveedores'
    ),

    path(
       'proveedores/nuevo/',
        proveedores_views.crear_proveedor,
        name='crear_proveedor'
    ),

    path(
       'proveedores/<int:proveedor_id>/editar/',
        proveedores_views.editar_proveedor,
        name='editar_proveedor'
    ),

    path(
       'proveedores/<int:proveedor_id>/eliminar/',
        proveedores_views.eliminar_proveedor,
        name='eliminar_proveedor'
    ),

    path(
       'movimientos/',
        movimientos_views.movimientos,
        name='movimientos'
    ),

    path(
       'movimientos/nuevo/',
        movimientos_views.crear_movimiento,
        name='crear_movimiento'
    ),

    path(
        'ventas/',
        ventas_views.ventas,
        name='ventas'
    ),

    path(
        'ventas/nuevo/',
        ventas_views.crear_venta,
        name='crear_venta'
    ),

    path('api/ventas/', include('ventas.urls')),
    path('api/productos/', include('productos.urls')),
    path('api/clientes/', include('clientes.urls')),
    path('api/proveedores/', include('proveedores.urls')),
    path('api/movimientos/', include('movimientos.urls')),
    
]
