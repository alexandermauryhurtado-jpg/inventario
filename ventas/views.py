from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Venta
from .services.ventas import registrar_venta

from clientes.models import Cliente
from productos.models import Producto

def lista_ventas(request):
    ventas = Venta.objects.select_related('cliente').prefetch_related(
        'detalles__producto'
    ).all()

    datos = []

    for venta in ventas:
        detalles = []

        for detalle in venta.detalles.all():
            detalles.append({
                'producto': detalle.producto.nombre,
                'cantidad': detalle.cantidad,
                'precio': str(detalle.precio),
                'subtotal': str(detalle.subtotal),
            })

        datos.append({
            'id': venta.id,
            'cliente': (
                venta.cliente.nombre
                if venta.cliente
                else 'Consumidor final'
            ),
            'fecha': venta.fecha,
            'total': str(venta.total),
            'estado': venta.estado,
            'detalles': detalles,
        })

    return JsonResponse(datos, safe=False)


def crear_venta(request):

    error = None

    clientes = Cliente.objects.filter(
        activo=True
    ).order_by('nombre')

    productos = Producto.objects.filter(
        activo=True,
        stock__gt=0
    ).order_by('nombre')

    if request.method == 'POST':

        try:

            # -------------------------
            # CLIENTE
            # -------------------------

            cliente_id = request.POST.get(
                'cliente',
                ''
            ).strip()

            if cliente_id:

                cliente = Cliente.objects.get(
                    id=cliente_id,
                    activo=True
                )

            else:

                cliente = None


            # -------------------------
            # PRODUCTOS DEL CARRITO
            # -------------------------

            cantidad_productos = int(
                request.POST.get(
                    'cantidad_productos',
                    0
                )
            )

            if cantidad_productos <= 0:

                raise ValueError(
                    'Debes agregar al menos un producto.'
                )


            productos_venta = []


            for i in range(cantidad_productos):

                producto_id = request.POST.get(
                    f'producto_{i}'
                )

                cantidad = int(
                    request.POST.get(
                        f'cantidad_{i}',
                        0
                    )
                )


                if not producto_id:

                    raise ValueError(
                        'Hay un producto inválido en la venta.'
                    )


                if cantidad <= 0:

                    raise ValueError(
                        'La cantidad debe ser mayor que cero.'
                    )


                producto = Producto.objects.get(
                    id=producto_id,
                    activo=True
                )


                productos_venta.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'precio': producto.precio_venta,
                })


            # -------------------------
            # REGISTRAR VENTA
            # -------------------------

            registrar_venta(
                cliente=cliente,
                productos=productos_venta
            )


            return redirect('ventas')


        except ValueError as e:

            error = str(e)


        except Cliente.DoesNotExist:

            error = (
                'El cliente seleccionado '
                'no existe o está inactivo.'
            )


        except Producto.DoesNotExist:

            error = (
                'Uno de los productos seleccionados '
                'no existe o está inactivo.'
            )


    return render(
        request,
        'ventas/nuevo.html',
        {
            'clientes': clientes,
            'productos': productos,
            'error': error,
        }
    )


def ventas(request):

    ventas = Venta.objects.select_related(
        'cliente'
    ).prefetch_related(
        'detalles__producto'
    ).order_by('-fecha')

    return render(
        request,
        'ventas/lista.html',
        {
            'ventas': ventas,
        }
    )