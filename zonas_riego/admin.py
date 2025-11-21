from django.contrib import admin
from .models import Zona


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_zona', 'area_m2', 'capacidad_agua_litros', 'estado', 'activa']
    list_filter = ['tipo_zona', 'estado', 'activa']
    search_fields = ['nombre', 'descripcion', 'ubicacion']
    ordering = ['nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'tipo_zona', 'ubicacion')
        }),
        ('Capacidades', {
            'fields': ('area_m2', 'capacidad_agua_litros')
        }),
        ('Estado', {
            'fields': ('estado', 'activa')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
