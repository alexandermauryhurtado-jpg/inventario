from django.shortcuts import render
from django.db.models import Sum, F

from productos.models import Producto
from clientes.models import Cliente
from proveedores.models import Proveedor
from ventas.models import Venta
from movimientos.models import Movimiento


def inicio(request):

    productos_stock_bajo = Producto.objects.filter(
        activo=True,
        stock__lte=F('stock_minimo')
    )

    ultimas_ventas = Venta.objects.select_related(
        'cliente'
    ).order_by('-fecha')[:5]

    ultimos_movimientos = Movimiento.objects.select_related(
        'producto',
        'proveedor'
    ).order_by('-fecha')[:5]

    contexto = {
        'total_productos': Producto.objects.filter(activo=True).count(),
        'total_clientes': Cliente.objects.filter(activo=True).count(),
        'total_proveedores': Proveedor.objects.filter(activo=True).count(),
        'total_ventas': Venta.objects.count(),
        'ultimos_movimientos': ultimos_movimientos,

        'stock_total': Producto.objects.filter(
            activo=True
        ).aggregate(
            total=Sum('stock')
        )['total'] or 0,

        'productos_stock_bajo': productos_stock_bajo,
        'ultimas_ventas': ultimas_ventas,
    }

    return render(
        request,
        'dashboard/inicio.html',
        contexto
    )