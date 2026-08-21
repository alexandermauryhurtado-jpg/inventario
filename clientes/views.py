from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q

from .models import Cliente


def lista_clientes(request):
    clientes = Cliente.objects.filter(activo=True)

    datos = []

    for cliente in clientes:
        datos.append({
            'id': cliente.id,
            'nombre': cliente.nombre,
            'documento': cliente.documento,
            'telefono': cliente.telefono,
            'correo': cliente.correo,
            'direccion': cliente.direccion,
            'ciudad': cliente.ciudad,
            'activo': cliente.activo,
        })

    return JsonResponse(datos, safe=False)


def clientes(request):


    busqueda = request.GET.get('buscar', '').strip()

    clientes = Cliente.objects.filter(activo=True)

    if busqueda:
        clientes = clientes.filter(
            Q(nombre__icontains=busqueda) |
            Q(documento__icontains=busqueda) |
            Q(telefono__icontains=busqueda) |
            Q(correo__icontains=busqueda)
        )

    clientes = clientes.order_by('nombre')

    return render(
        request,
        'clientes/lista.html',
        {
            'clientes': clientes,
            'busqueda': busqueda,
        }
    )


def crear_cliente(request):

    error = None

    if request.method == 'POST':

        documento = request.POST['documento'].strip()

        if Cliente.objects.filter(documento=documento).exists():

            error = 'Ya existe un cliente registrado con ese documento.'

        else:

            Cliente.objects.create(
                nombre=request.POST['nombre'],
                documento=documento,
                telefono=request.POST['telefono'],
                correo=request.POST['correo'],
                direccion=request.POST['direccion'],
                ciudad=request.POST['ciudad'],
            )

            return redirect('clientes')

    return render(
        request,
        'clientes/nuevo.html',
        {
            'error': error,
        }
    )

def editar_cliente(request, cliente_id):

    cliente = Cliente.objects.get(
        id=cliente_id,
        activo=True
    )

    error = None

    if request.method == 'POST':

        documento = request.POST['documento'].strip()

        if Cliente.objects.filter(
            documento=documento
        ).exclude(id=cliente.id).exists():

            error = 'Ya existe otro cliente registrado con ese documento.'

        else:

            cliente.nombre = request.POST['nombre']
            cliente.documento = documento
            cliente.telefono = request.POST['telefono']
            cliente.correo = request.POST['correo']
            cliente.direccion = request.POST['direccion']
            cliente.ciudad = request.POST['ciudad']

            cliente.save()

            return redirect('clientes')

    return render(
        request,
        'clientes/editar.html',
        {
            'cliente': cliente,
            'error': error,
        }
    )


def eliminar_cliente(request, cliente_id):

    cliente = Cliente.objects.get(
        id=cliente_id,
        activo=True
    )

    cliente.activo = False
    cliente.save()

    return redirect('clientes')