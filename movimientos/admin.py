from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Movimiento
from .services.inventario import registrar_movimiento


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = (
        'producto',
        'tipo',
        'cantidad',
        'proveedor',
        'motivo',
        'fecha',
    )

    search_fields = (
        'producto__nombre',
        'producto__codigo',
        'motivo',
    )

    list_filter = (
        'tipo',
        'fecha',
    )

    readonly_fields = (
        'fecha',
    )

    def save_model(self, request, obj, form, change):
        if change:
            raise ValidationError(
                'Los movimientos existentes no se pueden modificar.'
            )

        movimiento = registrar_movimiento(
            producto=obj.producto,
            tipo=obj.tipo,
            cantidad=obj.cantidad,
            proveedor=obj.proveedor,
            motivo=obj.motivo,
            observaciones=obj.observaciones,
        )

        obj.pk = movimiento.pk