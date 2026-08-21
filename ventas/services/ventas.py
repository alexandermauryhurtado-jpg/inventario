from django.db import transaction

from ventas.models import Venta, DetalleVenta
from productos.models import Producto
from movimientos.services.inventario import registrar_movimiento


@transaction.atomic
def registrar_venta(cliente, productos):
    """
    Registra una venta completa.

    productos debe ser una lista de diccionarios con:
    {
        'producto': producto,
        'cantidad': cantidad,
        'precio': precio
    }
    """

    if not productos:
        raise ValueError('La venta debe tener al menos un producto.')

    # Crear la venta inicialmente
    venta = Venta.objects.create(
        cliente=cliente,
        estado='PENDIENTE',
        total=0
    )

    total = 0

    for item in productos:
        producto = item['producto']
        cantidad = item['cantidad']
        precio = item['precio']

        if cantidad <= 0:
            raise ValueError(
                'La cantidad debe ser mayor que cero.'
            )

        # Bloqueamos el producto mientras se procesa la venta
        producto = Producto.objects.select_for_update().get(
            pk=producto.pk
        )

        # Verificar stock
        if cantidad > producto.stock:
            raise ValueError(
                f'Stock insuficiente para {producto.nombre}. '
                f'Stock disponible: {producto.stock}'
            )

        # Calcular subtotal
        subtotal = precio * cantidad

        # Crear detalle
        DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio=precio,
            subtotal=subtotal
        )

       
             # Registrar movimiento de salida
        registrar_movimiento(
            producto=producto,
            tipo='SALIDA',
            cantidad=cantidad,
            motivo=f'Venta #{venta.id}',
            observaciones=f'Salida generada automáticamente por la venta #{venta.id}'
        )

        

        # Acumular total
        total += subtotal

    # Actualizar la venta
    venta.total = total
    venta.estado = 'CONFIRMADA'
    venta.save(
        update_fields=['total', 'estado']
    )

    return venta