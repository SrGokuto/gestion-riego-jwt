from django.db import models


class Sensor(models.Model):
    TIPO_CHOICES = [
        ('HUMEDAD', 'Humedad'),
        ('TEMPERATURA', 'Temperatura'),
    ]
    nombre = models.CharField(max_length=120)
    ubicacion = models.CharField(max_length=200, blank=True)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Lectura(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='lecturas')
    humedad = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_hora = models.DateTimeField()
    nota = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"Lectura {self.humedad} @ {self.fecha_hora}"
