from rest_framework import serializers
from .models import Zona
from django.utils import timezone


class ZonaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Zona"""
    tipo_zona_display = serializers.CharField(source='get_tipo_zona_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    consumo_estimado = serializers.SerializerMethodField()
    
    class Meta:
        model = Zona
        fields = [
            'id', 'nombre', 'descripcion', 'tipo_zona', 'tipo_zona_display',
            'area_m2', 'capacidad_agua_litros', 'estado', 'estado_display',
            'ubicacion', 'activa', 'fecha_creacion', 'fecha_actualizacion',
            'consumo_estimado'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def get_consumo_estimado(self, obj):
        """Calcula el consumo estimado por m2"""
        if obj.area_m2 > 0:
            return float(obj.capacidad_agua_litros / obj.area_m2)
        return 0
    
    def validate_nombre(self, value):
        """Validación personalizada para el nombre"""
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        
        # Verificar que no contenga caracteres especiales problemáticos
        if any(char in value for char in ['<', '>', '/', '\\']):
            raise serializers.ValidationError(
                "El nombre no puede contener los caracteres: < > / \\"
            )
        
        return value.strip()
    
    def validate_area_m2(self, value):
        """Validación del área"""
        if value <= 0:
            raise serializers.ValidationError("El área debe ser mayor que cero.")
        
        if value > 100000:  # 10 hectáreas máximo
            raise serializers.ValidationError(
                "El área no puede ser mayor a 100,000 m²."
            )
        
        return value
    
    def validate(self, data):
        """Validaciones cruzadas"""
        area_m2 = data.get('area_m2')
        capacidad_agua_litros = data.get('capacidad_agua_litros')
        
        if area_m2 and capacidad_agua_litros:
            ratio = capacidad_agua_litros / area_m2
            if ratio > 100:
                raise serializers.ValidationError({
                    'capacidad_agua_litros': 
                    'La capacidad de agua es demasiado alta para el área especificada (máx. 100 L/m²).'
                })
            
            if ratio < 0.5:
                raise serializers.ValidationError({
                    'capacidad_agua_litros': 
                    'La capacidad de agua es demasiado baja para el área especificada (mín. 0.5 L/m²).'
                })
        
        return data


class ZonaSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple para listar zonas sin detalles completos"""
    tipo_zona_display = serializers.CharField(source='get_tipo_zona_display', read_only=True)
    
    class Meta:
        model = Zona
        fields = ['id', 'nombre', 'tipo_zona', 'tipo_zona_display', 'estado', 'area_m2']
