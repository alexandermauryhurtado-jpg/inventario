from django.db import transaction
from productos.models import Producto
from movimientos.models import Movimiento


@transaction.atomic
def registrar_movimiento(
    producto,
    tipo,
    cantidad,
    proveedor=None,
    motivo='',
    observaciones=''
):
    if cantidad <= 0:
        raise ValueError('La cantidad debe ser mayor que cero.')

    producto = Producto.objects.select_for_update().get(pk=producto.pk)

    if tipo == 'ENTRADA':
        producto.stock += cantidad

    elif tipo == 'SALIDA':
        if cantidad > producto.stock:
            raise ValueError(
                f'Stock insuficiente. Stock disponible: {producto.stock}'
            )

        producto.stock -= cantidad

    else:
        raise ValueError('Tipo de movimiento no válido.')

    producto.save(update_fields=['stock', 'fecha_actualizacion'])

    movimiento = Movimiento.objects.create(
        producto=producto,
        tipo=tipo,
        cantidad=cantidad,
        proveedor=proveedor,
        motivo=motivo,
        observaciones=observaciones
    )

    return movimiento