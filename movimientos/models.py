from django.db import models
from productos.models import Producto
from proveedores.models import Proveedor


class Movimiento(models.Model):

    TIPO_MOVIMIENTO = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='movimientos'
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_MOVIMIENTO
    )

    cantidad = models.PositiveIntegerField()

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name='movimientos',
        null=True,
        blank=True
    )

    motivo = models.CharField(
        max_length=200,
        blank=True
    )

    observaciones = models.TextField(
        blank=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} - {self.cantidad}"