import django_filters
from .models import Programacion


class ProgramacionFilter(django_filters.FilterSet):
    """Filtros para el modelo Programacion"""
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    zona = django_filters.NumberFilter(field_name='zona__id')
    zona_nombre = django_filters.CharFilter(field_name='zona__nombre', lookup_expr='icontains')
    frecuencia = django_filters.ChoiceFilter(choices=Programacion.FRECUENCIA_CHOICES)
    activa = django_filters.BooleanFilter()
    fecha_inicio_desde = django_filters.DateFilter(field_name='fecha_inicio', lookup_expr='gte')
    fecha_inicio_hasta = django_filters.DateFilter(field_name='fecha_inicio', lookup_expr='lte')
    fecha_fin_desde = django_filters.DateFilter(field_name='fecha_fin', lookup_expr='gte')
    fecha_fin_hasta = django_filters.DateFilter(field_name='fecha_fin', lookup_expr='lte')
    duracion_min = django_filters.NumberFilter(field_name='duracion_minutos', lookup_expr='gte')
    duracion_max = django_filters.NumberFilter(field_name='duracion_minutos', lookup_expr='lte')
    prioridad_min = django_filters.NumberFilter(field_name='prioridad', lookup_expr='gte')
    prioridad_max = django_filters.NumberFilter(field_name='prioridad', lookup_expr='lte')
    
    class Meta:
        model = Programacion
        fields = [
            'nombre', 'zona', 'zona_nombre', 'frecuencia', 'activa',
            'fecha_inicio_desde', 'fecha_inicio_hasta',
            'fecha_fin_desde', 'fecha_fin_hasta',
            'duracion_min', 'duracion_max',
            'prioridad_min', 'prioridad_max'
        ]
