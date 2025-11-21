from django.contrib import admin
from .models import Programacion


@admin.register(Programacion)
class ProgramacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'zona', 'hora_inicio', 'duracion_minutos', 'frecuencia', 'activa']
    list_filter = ['frecuencia', 'activa', 'zona']
    search_fields = ['nombre', 'descripcion']
    ordering = ['-prioridad', 'hora_inicio']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('zona', 'nombre', 'descripcion')
        }),
        ('Horario y Duración', {
            'fields': ('hora_inicio', 'duracion_minutos', 'caudal_litros_minuto')
        }),
        ('Frecuencia', {
            'fields': ('frecuencia', 'dias_semana', 'fecha_inicio', 'fecha_fin')
        }),
        ('Prioridad y Estado', {
            'fields': ('prioridad', 'activa')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
