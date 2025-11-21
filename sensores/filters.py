from django_filters import rest_framework as filters
from .models import Lectura


class LecturaFilter(filters.FilterSet):
    fecha_min = filters.DateTimeFilter(field_name='fecha_hora', lookup_expr='gte')
    fecha_max = filters.DateTimeFilter(field_name='fecha_hora', lookup_expr='lte')
    humedad_min = filters.NumberFilter(field_name='humedad', lookup_expr='gte')
    humedad_max = filters.NumberFilter(field_name='humedad', lookup_expr='lte')

    class Meta:
        model = Lectura
        fields = ['sensor', 'fecha_min', 'fecha_max', 'humedad_min', 'humedad_max']
