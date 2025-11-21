from django.db import models

class Medidor(models.Model):
    numero_serie = models.CharField(max_length=100, unique=True)
    ubicacion = models.CharField(max_length=200, blank=True)
    instalado = models.DateField()

    def __str__(self):
        return f"Medidor {self.numero_serie}"

class Consumo(models.Model):
    medidor = models.ForeignKey(Medidor, on_delete=models.CASCADE, related_name='consumos')
    fecha = models.DateField()
    volumen_m3 = models.DecimalField(max_digits=8, decimal_places=2)
    observacion = models.TextField(blank=True)

    class Meta:
        unique_together = ('medidor', 'fecha')
        ordering = ['-fecha']

    def __str__(self):
        return f"Consumo {self.medidor.numero_serie} - {self.fecha}: {self.volumen_m3} m3"
