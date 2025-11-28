from rest_framework import viewsets, decorators, response
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from .models import Medidor, Consumo
from .serializers import MedidorSerializer, ConsumoSerializer
from .filters import ConsumoFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class MedidorViewSet(viewsets.ModelViewSet):
    queryset = Medidor.objects.all()
    serializer_class = MedidorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    @decorators.action(detail=True, methods=['get'])
    def total_consumo(self, request, pk=None):
        medidor = self.get_object()
        qs = medidor.consumos.all()
        fecha_min = request.query_params.get('fecha_min')
        fecha_max = request.query_params.get('fecha_max')
        if fecha_min:
            qs = qs.filter(fecha__gte=fecha_min)
        if fecha_max:
            qs = qs.filter(fecha__lte=fecha_max)
        total = qs.aggregate(total=Sum('volumen_m3'))['total']
        return response.Response({'medidor': medidor.numero_serie, 'total_consumo_m3': total})

class ConsumoViewSet(viewsets.ModelViewSet):
    queryset = Consumo.objects.all()
    serializer_class = ConsumoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConsumoFilter
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
