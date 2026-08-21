from django.contrib import admin
from .models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'documento',
        'telefono',
        'correo',
        'ciudad',
        'activo',
    )

    search_fields = (
        'nombre',
        'documento',
    )

    list_filter = (
        'activo',
        'ciudad',
    )
