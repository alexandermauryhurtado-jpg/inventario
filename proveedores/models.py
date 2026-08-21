from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    documento = models.CharField(max_length=30, unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    correo = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    ciudad = models.CharField(max_length=100, default='Barranquilla')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre