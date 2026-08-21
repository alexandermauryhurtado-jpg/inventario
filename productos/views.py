from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse

from .models import Producto


def lista_productos(request):
    productos = Producto.objects.all()

    datos = []

    for producto in productos:
        datos.append({
            'id': producto.id,
            'codigo': producto.codigo,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio_compra': str(producto.precio_compra),
            'precio_venta': str(producto.precio_venta),
            'stock': producto.stock,
            'stock_minimo': producto.stock_minimo,
            'activo': producto.activo,
        })

    return JsonResponse(datos, safe=False)


def productos(request):

    busqueda = request.GET.get('buscar', '').strip()

    productos = Producto.objects.filter(activo=True)

    if busqueda:
        productos = productos.filter(
            Q(codigo__icontains=busqueda) |
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    productos = productos.order_by('nombre')

    return render(
        request,
        'productos/lista.html',
        {
            'productos': productos,
            'busqueda': busqueda,
        }
    )


def crear_producto(request):

    if request.method == 'POST':

        Producto.objects.create(
            codigo=request.POST['codigo'],
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion'],
            precio_compra=request.POST['precio_compra'],
            precio_venta=request.POST['precio_venta'],
            stock=request.POST['stock'],
            stock_minimo=request.POST['stock_minimo'],
            activo=True,
        )

        return redirect('productos')

    return render(
        request,
        'productos/crear.html'
    )


def editar_producto(request, producto_id):

    producto = Producto.objects.get(id=producto_id)

    if request.method == 'POST':

        producto.codigo = request.POST['codigo']
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST['descripcion']
        producto.precio_compra = request.POST['precio_compra']
        producto.precio_venta = request.POST['precio_venta']
        producto.stock = request.POST['stock']
        producto.stock_minimo = request.POST['stock_minimo']

        producto.save()

        return redirect('productos')

    return render(
        request,
        'productos/editar.html',
        {
            'producto': producto,
        }
    )



def eliminar_producto(request, producto_id):

    producto = Producto.objects.get(id=producto_id)

    producto.activo = False
    producto.save()

    return redirect('productos')