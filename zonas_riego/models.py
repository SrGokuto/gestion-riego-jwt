from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Zona(models.Model):
    """
    Modelo para representar una zona de riego
    """
    TIPO_ZONA_CHOICES = [
        ('jardin', 'Jardín'),
        ('huerto', 'Huerto'),
        ('cesped', 'Césped'),
        ('cultivo', 'Cultivo'),
        ('ornamental', 'Ornamental'),
    ]
    
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
        ('mantenimiento', 'Mantenimiento'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    tipo_zona = models.CharField(max_length=20, choices=TIPO_ZONA_CHOICES, default='jardin')
    area_m2 = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Área de la zona en metros cuadrados"
    )
    capacidad_agua_litros = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Capacidad de agua en litros"
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Zona de Riego'
        verbose_name_plural = 'Zonas de Riego'
        ordering = ['nombre']
        
    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_zona_display()}"
    
    def clean(self):
        """Validaciones personalizadas"""
        super().clean()
        if self.capacidad_agua_litros and self.area_m2:
            # Validar que la capacidad de agua sea proporcional al área
            ratio = self.capacidad_agua_litros / self.area_m2
            if ratio > 100:  # Máximo 100 litros por m2
                raise ValidationError({
                    'capacidad_agua_litros': 'La capacidad de agua es demasiado alta para el área especificada.'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
