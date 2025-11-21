from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from zonas_riego.models import Zona
from django.utils import timezone


class Programacion(models.Model):
    """
    Modelo para representar programaciones de riego
    """
    DIAS_SEMANA_CHOICES = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]
    
    FRECUENCIA_CHOICES = [
        ('diaria', 'Diaria'),
        ('semanal', 'Semanal'),
        ('quincenal', 'Quincenal'),
        ('mensual', 'Mensual'),
        ('personalizada', 'Personalizada'),
    ]
    
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('pausada', 'Pausada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    zona = models.ForeignKey(
        Zona,
        on_delete=models.CASCADE,
        related_name='programaciones'
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    hora_inicio = models.TimeField(help_text="Hora de inicio del riego")
    duracion_minutos = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1440)],
        help_text="Duración del riego en minutos (máx. 24 horas)"
    )
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIA_CHOICES, default='diaria')
    dias_semana = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de días de la semana para riego semanal"
    )
    fecha_inicio = models.DateField(help_text="Fecha de inicio de la programación")
    fecha_fin = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de fin de la programación (opcional)"
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    caudal_litros_minuto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
        help_text="Caudal de agua en litros por minuto"
    )
    prioridad = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Prioridad de la programación (1=baja, 10=alta)"
    )
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Programación de Riego'
        verbose_name_plural = 'Programaciones de Riego'
        ordering = ['-prioridad', 'hora_inicio']
        
    def __str__(self):
        return f"{self.nombre} - {self.zona.nombre} ({self.get_frecuencia_display()})"
    
    def clean(self):
        """Validaciones personalizadas"""
        super().clean()
        
        # Validar fechas
        if self.fecha_fin and self.fecha_inicio:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError({
                    'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio.'
                })
        
        # Validar días de la semana para frecuencia semanal
        if self.frecuencia == 'semanal' and not self.dias_semana:
            raise ValidationError({
                'dias_semana': 'Debe especificar al menos un día de la semana para frecuencia semanal.'
                })
        
        # Validar consumo total
        if self.duracion_minutos and self.caudal_litros_minuto:
            consumo_total = float(self.duracion_minutos * self.caudal_litros_minuto)
            if self.zona and consumo_total > float(self.zona.capacidad_agua_litros):
                raise ValidationError({
                    'duracion_minutos': f'El consumo total ({consumo_total}L) supera la capacidad de la zona ({self.zona.capacidad_agua_litros}L).'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def consumo_total_litros(self):
        """Calcula el consumo total de agua en litros"""
        return float(self.duracion_minutos * self.caudal_litros_minuto)
    
    @property
    def esta_vigente(self):
        """Verifica si la programación está vigente"""
        hoy = timezone.now().date()
        if hoy < self.fecha_inicio:
            return False
        if self.fecha_fin and hoy > self.fecha_fin:
            return False
        return True
