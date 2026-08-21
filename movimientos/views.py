from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Movimiento
from .services.inventario import registrar_movimiento

from productos.models import Producto
from proveedores.models import Proveedor

def lista_movimientos(request):
    movimientos = Movimiento.objects.select_related(
        'producto',
        'proveedor',
    ).all()

    datos = []

    for movimiento in movimientos:
        datos.append({
            'id': movimiento.id,
            'producto': movimiento.producto.nombre,
            'tipo': movimiento.tipo,
            'cantidad': movimiento.cantidad,
            'proveedor': (
                movimiento.proveedor.nombre
                if movimiento.proveedor
                else None
            ),
            'motivo': movimiento.motivo,
            'observaciones': movimiento.observaciones,
            'fecha': movimiento.fecha,
        })

    return JsonResponse(datos, safe=False)


def movimientos(request):

    movimientos = Movimiento.objects.select_related(
        'producto',
        'proveedor'
    ).order_by('-fecha')

    return render(
        request,
        'movimientos/lista.html',
        {
            'movimientos': movimientos,
        }
    )


def crear_movimiento(request):

    error = None

    productos = Producto.objects.filter(
        activo=True
    ).order_by('nombre')

    proveedores = Proveedor.objects.filter(
        activo=True
    ).order_by('nombre')

    if request.method == 'POST':

        try:

            producto_id = request.POST['producto']
            tipo = request.POST['tipo']
            cantidad = int(request.POST['cantidad'])
            proveedor_id = request.POST.get('proveedor')

            motivo = request.POST.get('motivo', '').strip()
            observaciones = request.POST.get(
                'observaciones',
                ''
            ).strip()

            producto = Producto.objects.get(
                id=producto_id,
                activo=True
            )

            proveedor = None

            if proveedor_id:
                proveedor = Proveedor.objects.get(
                    id=proveedor_id,
                    activo=True
                )

            registrar_movimiento(
                producto=producto,
                tipo=tipo,
                cantidad=cantidad,
                proveedor=proveedor,
                motivo=motivo,
                observaciones=observaciones
            )

            return redirect('movimientos')

        except ValueError as e:

            error = str(e)

        except Producto.DoesNotExist:

            error = 'El producto seleccionado no existe o está inactivo.'

        except Proveedor.DoesNotExist:

            error = 'El proveedor seleccionado no existe o está inactivo.'

    return render(
        request,
        'movimientos/nuevo.html',
        {
            'productos': productos,
            'proveedores': proveedores,
            'error': error,
        }
    )