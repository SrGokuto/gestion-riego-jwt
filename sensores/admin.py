from django.contrib import admin
from .models import Sensor, Lectura


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'ubicacion', 'creado')


@admin.register(Lectura)
class LecturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sensor', 'humedad', 'fecha_hora')
