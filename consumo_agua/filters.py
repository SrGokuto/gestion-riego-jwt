from django_filters import rest_framework as filters
from .models import Consumo

class ConsumoFilter(filters.FilterSet):
    fecha_min = filters.DateFilter(field_name='fecha', lookup_expr='gte')
    fecha_max = filters.DateFilter(field_name='fecha', lookup_expr='lte')
    volumen_min = filters.NumberFilter(field_name='volumen_m3', lookup_expr='gte')
    volumen_max = filters.NumberFilter(field_name='volumen_m3', lookup_expr='lte')

    class Meta:
        model = Consumo
        fields = ['medidor', 'fecha_min', 'fecha_max', 'volumen_min', 'volumen_max']
