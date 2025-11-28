from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import Zona
from .serializers import ZonaSerializer, ZonaSimpleSerializer
from .filters import ZonaFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ZonaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Zonas de Riego
    
    Endpoints:
    - GET /api/zonas/ - Listar todas las zonas
    - POST /api/zonas/ - Crear una nueva zona
    - GET /api/zonas/{id}/ - Obtener detalle de una zona
    - PUT /api/zonas/{id}/ - Actualizar completamente una zona
    - PATCH /api/zonas/{id}/ - Actualizar parcialmente una zona
    - DELETE /api/zonas/{id}/ - Eliminar una zona
    - GET /api/zonas/estadisticas/ - Estadísticas generales
    - GET /api/zonas/{id}/resumen/ - Resumen de una zona específica
    """
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer
    filterset_class = ZonaFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion', 'ubicacion']
    ordering_fields = ['nombre', 'area_m2', 'capacidad_agua_litros', 'fecha_creacion']
    ordering = ['nombre']

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Usar serializer simple para listado"""
        if self.action == 'list':
            return ZonaSimpleSerializer
        return ZonaSerializer
    
    @swagger_auto_schema(
        operation_description="Obtener estadísticas generales de todas las zonas",
        responses={
            200: openapi.Response(
                description="Estadísticas calculadas",
                examples={
                    "application/json": {
                        "total_zonas": 10,
                        "zonas_activas": 8,
                        "zonas_inactivas": 2,
                        "area_total_m2": "5000.00",
                        "capacidad_total_litros": "250000.00",
                        "promedio_area_m2": "500.00",
                        "promedio_capacidad_litros": "25000.00",
                        "zonas_por_tipo": {
                            "jardin": 3,
                            "huerto": 5,
                            "cesped": 2
                        },
                        "zonas_por_estado": {
                            "activa": 7,
                            "mantenimiento": 3
                        }
                    }
                }
            )
        }
    )
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Endpoint para obtener estadísticas generales de zonas"""
        queryset = self.get_queryset()
        
        # Estadísticas básicas
        stats = queryset.aggregate(
            total_zonas=Count('id'),
            zonas_activas=Count('id', filter=Q(activa=True)),
            zonas_inactivas=Count('id', filter=Q(activa=False)),
            area_total_m2=Sum('area_m2'),
            capacidad_total_litros=Sum('capacidad_agua_litros'),
            promedio_area_m2=Avg('area_m2'),
            promedio_capacidad_litros=Avg('capacidad_agua_litros'),
        )
        
        # Zonas por tipo
        zonas_por_tipo = {}
        for tipo_choice in Zona.TIPO_ZONA_CHOICES:
            tipo_key = tipo_choice[0]
            count = queryset.filter(tipo_zona=tipo_key).count()
            if count > 0:
                zonas_por_tipo[tipo_key] = count
        
        # Zonas por estado
        zonas_por_estado = {}
        for estado_choice in Zona.ESTADO_CHOICES:
            estado_key = estado_choice[0]
            count = queryset.filter(estado=estado_key).count()
            if count > 0:
                zonas_por_estado[estado_key] = count
        
        stats['zonas_por_tipo'] = zonas_por_tipo
        stats['zonas_por_estado'] = zonas_por_estado
        
        return Response(stats)
    
    @swagger_auto_schema(
        operation_description="Obtener resumen detallado de una zona específica",
        responses={
            200: openapi.Response(
                description="Resumen de la zona",
                examples={
                    "application/json": {
                        "zona": {
                            "id": 1,
                            "nombre": "Jardín Principal"
                        },
                        "capacidad_agua_total": "5000.00",
                        "area_total": "100.00",
                        "ratio_agua_area": "50.00",
                        "estado_actual": "activa"
                    }
                }
            )
        }
    )
    @action(detail=True, methods=['get'])
    def resumen(self, request, pk=None):
        """Endpoint para obtener un resumen detallado de una zona"""
        zona = self.get_object()
        
        data = {
            'zona': {
                'id': zona.id,
                'nombre': zona.nombre,
                'tipo': zona.get_tipo_zona_display(),
                'estado': zona.get_estado_display()
            },
            'capacidad_agua_total': float(zona.capacidad_agua_litros),
            'area_total': float(zona.area_m2),
            'ratio_agua_area': float(zona.capacidad_agua_litros / zona.area_m2) if zona.area_m2 > 0 else 0,
            'estado_actual': zona.estado,
            'activa': zona.activa,
            'ubicacion': zona.ubicacion or 'No especificada'
        }
        
        return Response(data)
