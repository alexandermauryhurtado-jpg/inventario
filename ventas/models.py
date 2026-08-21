from django.db import models
from clientes.models import Cliente


class Venta(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='ventas',
        null=True,
        blank=True
    )

    fecha = models.DateTimeField(auto_now_add=True)

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='PENDIENTE'
    )

    def __str__(self):
        return f'Venta #{self.id} - {self.cliente}'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        'productos.Producto',
        on_delete=models.PROTECT,
        related_name='detalles_venta'
    )

    cantidad = models.PositiveIntegerField()

    precio = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f'{self.producto} x {self.cantidad}'