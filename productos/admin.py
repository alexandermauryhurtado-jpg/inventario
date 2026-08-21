from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'nombre',
        'precio_compra',
        'precio_venta',
        'stock',
        'stock_minimo',
        'activo',
    )

    search_fields = (
        'codigo',
        'nombre',
    )

    list_filter = (
        'activo',
    )