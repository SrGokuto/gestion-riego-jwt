from rest_framework import serializers
from .models import Programacion
from zonas_riego.models import Zona
from django.utils import timezone
from datetime import datetime, time


class ProgramacionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Programacion"""
    zona_nombre = serializers.CharField(source='zona.nombre', read_only=True)
    frecuencia_display = serializers.CharField(source='get_frecuencia_display', read_only=True)
    consumo_total_litros = serializers.FloatField(read_only=True)
    esta_vigente = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Programacion
        fields = [
            'id', 'zona', 'zona_nombre', 'nombre', 'descripcion', 'frecuencia',
            'frecuencia_display', 'dias_semana', 'hora_inicio', 'fecha_inicio',
            'fecha_fin', 'caudal_litros_minuto', 'duracion_minutos', 'prioridad',
            'activa', 'fecha_creacion', 'fecha_actualizacion', 'consumo_total_litros',
            'esta_vigente'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def validate_nombre(self, value):
        """Validación personalizada para el nombre"""
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        
        return value.strip()
    
    def validate_caudal_litros_minuto(self, value):
        """Validación del caudal"""
        if value <= 0:
            raise serializers.ValidationError("El caudal debe ser mayor que cero.")
        
        if value > 1000:
            raise serializers.ValidationError(
                "El caudal no puede ser mayor a 1,000 litros por minuto."
            )
        
        return value
    
    def validate_duracion_minutos(self, value):
        """Validación de la duración"""
        if value <= 0:
            raise serializers.ValidationError("La duración debe ser mayor que cero.")
        
        if value > 480:  # 8 horas máximo
            raise serializers.ValidationError(
                "La duración no puede ser mayor a 480 minutos (8 horas)."
            )
        
        return value
    
    def validate_prioridad(self, value):
        """Validación de la prioridad"""
        if not (1 <= value <= 10):
            raise serializers.ValidationError("La prioridad debe estar entre 1 y 10.")
        
        return value
    
    def validate_dias_semana(self, value):
        """Validación de los días de la semana"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Los días de la semana deben ser una lista.")
        
        dias_validos = [0, 1, 2, 3, 4, 5, 6]
        if not all(dia in dias_validos for dia in value):
            raise serializers.ValidationError(
                "Los días deben ser números entre 0 (lunes) y 6 (domingo)."
            )
        
        return value
    
    def validate(self, data):
        """Validaciones cruzadas"""
        zona = data.get('zona')
        if zona and not zona.activa:
            raise serializers.ValidationError({
                'zona': 'No se puede crear una programación para una zona inactiva.'
            })
        
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        if fecha_fin and fecha_inicio:
            if fecha_fin < fecha_inicio:
                raise serializers.ValidationError({
                    'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio.'
                })
        
        # Validar que la frecuencia y los días de la semana sean consistentes
        frecuencia = data.get('frecuencia')
        dias_semana = data.get('dias_semana', [])
        
        if frecuencia == 'semanal' and not dias_semana:
            raise serializers.ValidationError({
                'dias_semana': 'Debe especificar al menos un día para la frecuencia semanal.'
            })
        
        return data


class ProgramacionSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple para listar programaciones sin detalles completos"""
    zona_nombre = serializers.CharField(source='zona.nombre', read_only=True)
    frecuencia_display = serializers.CharField(source='get_frecuencia_display', read_only=True)
    
    class Meta:
        model = Programacion
        fields = ['id', 'zona', 'zona_nombre', 'nombre', 'frecuencia', 'frecuencia_display', 'activa']
