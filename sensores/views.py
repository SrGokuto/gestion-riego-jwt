from rest_framework import viewsets, decorators, response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sensor, Lectura
from .serializers import SensorSerializer, LecturaSerializer
from .filters import LecturaFilter


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    # 🔐 Requerir JWT para acceder a todo el ViewSet
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @decorators.action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        sensor = self.get_object()
        qs = sensor.lecturas.all()

        # Filtros opcionales por fecha
        fecha_min = request.query_params.get('fecha_min')
        fecha_max = request.query_params.get('fecha_max')

        if fecha_min:
            qs = qs.filter(fecha_hora__gte=fecha_min)
        if fecha_max:
            qs = qs.filter(fecha_hora__lte=fecha_max)

        # Calcular promedio de humedad
        avg_humedad = qs.aggregate(avg=Avg('humedad'))['avg']

        return response.Response({
            'sensor': sensor.id,
            'avg_humedad': avg_humedad
        })


class LecturaViewSet(viewsets.ModelViewSet):
    queryset = Lectura.objects.all()
    serializer_class = LecturaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LecturaFilter

    # 🔐 También protegemos la API de lecturas
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
