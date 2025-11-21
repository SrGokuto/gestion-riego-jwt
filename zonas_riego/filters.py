import django_filters
from .models import Zona


class ZonaFilter(django_filters.FilterSet):
    """Filtros para el modelo Zona"""
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    tipo_zona = django_filters.ChoiceFilter(choices=Zona.TIPO_ZONA_CHOICES)
    estado = django_filters.ChoiceFilter(choices=Zona.ESTADO_CHOICES)
    area_m2_min = django_filters.NumberFilter(field_name='area_m2', lookup_expr='gte')
    area_m2_max = django_filters.NumberFilter(field_name='area_m2', lookup_expr='lte')
    capacidad_min = django_filters.NumberFilter(field_name='capacidad_agua_litros', lookup_expr='gte')
    capacidad_max = django_filters.NumberFilter(field_name='capacidad_agua_litros', lookup_expr='lte')
    fecha_creacion_desde = django_filters.DateTimeFilter(field_name='fecha_creacion', lookup_expr='gte')
    fecha_creacion_hasta = django_filters.DateTimeFilter(field_name='fecha_creacion', lookup_expr='lte')
    activa = django_filters.BooleanFilter()
    
    class Meta:
        model = Zona
        fields = [
            'nombre', 'tipo_zona', 'estado', 'activa',
            'area_m2_min', 'area_m2_max',
            'capacidad_min', 'capacidad_max',
            'fecha_creacion_desde', 'fecha_creacion_hasta'
        ]
