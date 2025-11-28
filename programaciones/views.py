from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Programacion
from .serializers import ProgramacionSerializer, ProgramacionSimpleSerializer
from .filters import ProgramacionFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated


class ProgramacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Programaciones de Riego
    
    Endpoints:
    - GET /api/programaciones/ - Listar todas las programaciones
    - POST /api/programaciones/ - Crear una nueva programación
    - GET /api/programaciones/{id}/ - Obtener detalle de una programación
    - PUT /api/programaciones/{id}/ - Actualizar completamente
    - PATCH /api/programaciones/{id}/ - Actualizar parcialmente
    - DELETE /api/programaciones/{id}/ - Eliminar una programación
    - GET /api/programaciones/vigentes/ - Listar programaciones vigentes
    - GET /api/programaciones/estadisticas/ - Estadísticas generales
    - POST /api/programaciones/{id}/ejecutar/ - Simular ejecución de riego
    """
    queryset = Programacion.objects.all()
    serializer_class = ProgramacionSerializer
    filterset_class = ProgramacionFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'hora_inicio', 'prioridad', 'fecha_creacion']
    ordering = ['-prioridad', 'hora_inicio']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Usar serializer simple para listado"""
        if self.action == 'list':
            return ProgramacionSimpleSerializer
        return ProgramacionSerializer
    
    @swagger_auto_schema(
        operation_description="Obtener programaciones vigentes (activas y dentro del rango de fechas)",
        responses={
            200: ProgramacionSimpleSerializer(many=True)
        }
    )
    @action(detail=False, methods=['get'])
    def vigentes(self, request):
        """Endpoint para listar solo las programaciones vigentes"""
        hoy = timezone.now().date()
        queryset = self.get_queryset().filter(
            activa=True,
            fecha_inicio__lte=hoy
        ).filter(
            Q(fecha_fin__gte=hoy) | Q(fecha_fin__isnull=True)
        )
        
        serializer = ProgramacionSimpleSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Obtener estadísticas generales de todas las programaciones",
        responses={
            200: openapi.Response(
                description="Estadísticas calculadas",
                examples={
                    "application/json": {
                        "total_programaciones": 15,
                        "programaciones_activas": 12,
                        "programaciones_inactivas": 3,
                        "programaciones_vigentes": 10,
                        "consumo_total_estimado_litros": 125000.50,
                        "duracion_total_minutos": 450,
                        "programaciones_por_frecuencia": {
                            "diaria": 5,
                            "semanal": 7,
                            "mensual": 3
                        }
                    }
                }
            )
        }
    )
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Endpoint para obtener estadísticas generales de programaciones"""
        queryset = self.get_queryset()
        hoy = timezone.now().date()
        
        # Contar programaciones vigentes
        vigentes_count = queryset.filter(
            activa=True,
            fecha_inicio__lte=hoy
        ).filter(
            Q(fecha_fin__gte=hoy) | Q(fecha_fin__isnull=True)
        ).count()
        
        # Estadísticas básicas
        stats = queryset.aggregate(
            total_programaciones=Count('id'),
            programaciones_activas=Count('id', filter=Q(activa=True)),
            programaciones_inactivas=Count('id', filter=Q(activa=False)),
            consumo_total_estimado_litros=Sum(
                F('caudal_litros_minuto') * F('duracion_minutos')
            ),
            duracion_total_minutos=Sum('duracion_minutos'),
            promedio_duracion=Avg('duracion_minutos'),
            promedio_caudal=Avg('caudal_litros_minuto'),
        )
        
        stats['programaciones_vigentes'] = vigentes_count
        
        # Programaciones por frecuencia
        programaciones_por_frecuencia = {}
        for frecuencia_choice in Programacion.FRECUENCIA_CHOICES:
            frecuencia_key = frecuencia_choice[0]
            count = queryset.filter(frecuencia=frecuencia_key).count()
            if count > 0:
                programaciones_por_frecuencia[frecuencia_key] = count
        
        stats['programaciones_por_frecuencia'] = programaciones_por_frecuencia
        
        return Response(stats)
    
    @swagger_auto_schema(
        operation_description="Simular la ejecución de una programación de riego",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'hora_inicio_real': openapi.Schema(type=openapi.TYPE_STRING, format='time', description='Hora de inicio real (HH:MM:SS)'),
                'duracion_real_minutos': openapi.Schema(type=openapi.TYPE_NUMBER, description='Duración real en minutos'),
                'observaciones': openapi.Schema(type=openapi.TYPE_STRING, description='Observaciones opcionales'),
            },
            required=[]
        ),
        responses={
            200: openapi.Response(
                description="Ejecución simulada exitosamente",
                examples={
                    "application/json": {
                        "success": True,
                        "mensaje": "Ejecución de riego simulada exitosamente",
                        "datos": {
                            "programacion_id": 1,
                            "zona_nombre": "Jardín Principal",
                            "hora_inicio": "08:00:00",
                            "duracion_minutos": 30,
                            "consumo_estimado_litros": 150.0
                        }
                    }
                }
            ),
            400: "Error en la simulación"
        }
    )
    @action(detail=True, methods=['post'])
    def ejecutar(self, request, pk=None):
        """Endpoint para simular la ejecución de una programación"""
        programacion = self.get_object()
        
        if not programacion.activa:
            return Response(
                {'error': 'La programación no está activa.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not programacion.zona.activa:
            return Response(
                {'error': 'La zona de riego no está activa.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Datos de la ejecución simulada
        hora_inicio_real = request.data.get('hora_inicio_real', programacion.hora_inicio)
        duracion_real = request.data.get('duracion_real_minutos', programacion.duracion_minutos)
        observaciones = request.data.get('observaciones', '')
        
        # Calcular consumo
        consumo_litros = float(programacion.caudal_litros_minuto * duracion_real)
        
        data = {
            'success': True,
            'mensaje': 'Ejecución de riego simulada exitosamente',
            'datos': {
                'programacion_id': programacion.id,
                'programacion_nombre': programacion.nombre,
                'zona_id': programacion.zona.id,
                'zona_nombre': programacion.zona.nombre,
                'hora_inicio': str(hora_inicio_real),
                'duracion_minutos': duracion_real,
                'caudal_litros_minuto': float(programacion.caudal_litros_minuto),
                'consumo_estimado_litros': consumo_litros,
                'observaciones': observaciones
            }
        }
        
        return Response(data)
