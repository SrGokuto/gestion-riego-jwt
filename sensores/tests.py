from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Sensor, Lectura
from django.utils import timezone


class SensoresAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sensor = Sensor.objects.create(nombre='Sensor 1', tipo='HUMEDAD')

    def test_create_sensor(self):
        data = {'nombre': 'Sensor X', 'tipo': 'HUMEDAD'}
        resp = self.client.post('/api/sensores/', data, format='json')
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK))

    def test_create_lectura_invalid_humedad(self):
        data = {
            'sensor': self.sensor.id,
            'humedad': 150,
            'fecha_hora': timezone.now().isoformat()
        }
        resp = self.client.post('/api/lecturas/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
