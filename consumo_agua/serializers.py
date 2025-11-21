from rest_framework import serializers
from .models import Medidor, Consumo

class MedidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medidor
        fields = '__all__'

class ConsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumo
        fields = '__all__'

    def validate_volumen_m3(self, value):
        if value < 0:
            raise serializers.ValidationError('El volumen debe ser positivo.')
        return value
