from rest_framework import viewsets, decorators, response
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sensor, Lectura
from .serializers import SensorSerializer, LecturaSerializer
from .filters import LecturaFilter


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    @decorators.action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        sensor = self.get_object()
        qs = sensor.lecturas.all()
        fecha_min = request.query_params.get('fecha_min')
        fecha_max = request.query_params.get('fecha_max')
        if fecha_min:
            qs = qs.filter(fecha_hora__gte=fecha_min)
        if fecha_max:
            qs = qs.filter(fecha_hora__lte=fecha_max)
        avg_humedad = qs.aggregate(avg=Avg('humedad'))['avg']
        return response.Response({'sensor': sensor.id, 'avg_humedad': avg_humedad})


class LecturaViewSet(viewsets.ModelViewSet):
    queryset = Lectura.objects.all()
    serializer_class = LecturaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LecturaFilter
