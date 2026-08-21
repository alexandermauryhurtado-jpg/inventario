from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q

from .models import Proveedor


def lista_proveedores(request):

    proveedores = Proveedor.objects.filter(activo=True)

    datos = []

    for proveedor in proveedores:
        datos.append({
            'id': proveedor.id,
            'nombre': proveedor.nombre,
            'documento': proveedor.documento,
            'telefono': proveedor.telefono,
            'correo': proveedor.correo,
            'direccion': proveedor.direccion,
            'ciudad': proveedor.ciudad,
            'activo': proveedor.activo,
        })

    return JsonResponse(datos, safe=False)


def proveedores(request):

    busqueda = request.GET.get('buscar', '').strip()

    proveedores = Proveedor.objects.filter(activo=True)

    if busqueda:
        proveedores = proveedores.filter(
            Q(nombre__icontains=busqueda) |
            Q(documento__icontains=busqueda) |
            Q(telefono__icontains=busqueda) |
            Q(correo__icontains=busqueda)
        )

    proveedores = proveedores.order_by('nombre')

    return render(
        request,
        'proveedores/lista.html',
        {
            'proveedores': proveedores,
            'busqueda': busqueda,
        }
    )


def crear_proveedor(request):

    error = None

    if request.method == 'POST':

        documento = request.POST['documento'].strip()

        if Proveedor.objects.filter(documento=documento).exists():

            error = 'Ya existe un proveedor registrado con ese documento.'

        else:

            Proveedor.objects.create(
                nombre=request.POST['nombre'],
                documento=documento,
                telefono=request.POST['telefono'],
                correo=request.POST['correo'],
                direccion=request.POST['direccion'],
                ciudad=request.POST['ciudad'],
            )

            return redirect('proveedores')

    return render(
        request,
        'proveedores/nuevo.html',
        {
            'error': error,
        }
    )


def editar_proveedor(request, proveedor_id):

    proveedor = Proveedor.objects.get(
        id=proveedor_id,
        activo=True
    )

    error = None

    if request.method == 'POST':

        documento = request.POST['documento'].strip()

        if Proveedor.objects.filter(
            documento=documento
        ).exclude(id=proveedor_id).exists():

            error = 'Ya existe otro proveedor registrado con ese documento.'

        else:

            proveedor.nombre = request.POST['nombre']
            proveedor.documento = documento
            proveedor.telefono = request.POST['telefono']
            proveedor.correo = request.POST['correo']
            proveedor.direccion = request.POST['direccion']
            proveedor.ciudad = request.POST['ciudad']

            proveedor.save()

            return redirect('proveedores')

    return render(
        request,
        'proveedores/editar.html',
        {
            'proveedor': proveedor,
            'error': error,
        }
    )


def eliminar_proveedor(request, proveedor_id):

    proveedor = Proveedor.objects.get(
        id=proveedor_id,
        activo=True
    )

    proveedor.activo = False
    proveedor.save()

    return redirect('proveedores')