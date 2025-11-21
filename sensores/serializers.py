from rest_framework import serializers
from .models import Sensor, Lectura
from django.utils import timezone


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class LecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lectura
        fields = '__all__'

    def validate_humedad(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError('La humedad debe estar entre 0 y 100.')
        return value

    def validate(self, data):
        fecha = data.get('fecha_hora')
        if fecha and fecha > timezone.now() + timezone.timedelta(minutes=5):
            raise serializers.ValidationError('fecha_hora no puede ser futura.')
        return data
