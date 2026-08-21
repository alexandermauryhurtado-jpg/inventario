from django.contrib import admin

from .models import Venta, DetalleVenta


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'fecha',
        'total',
        'estado',
    )

    search_fields = (
        'cliente__nombre',
        'cliente__documento',
    )

    list_filter = (
        'estado',
        'fecha',
    )

    readonly_fields = (
        'fecha',
        'total',
    )

    inlines = [
        DetalleVentaInline,
    ]


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = (
        'venta',
        'producto',
        'cantidad',
        'precio',
        'subtotal',
    )

    search_fields = (
        'producto__nombre',
        'producto__codigo',
    )