"""
Script para crear datos de ejemplo en la base de datos
Ejecutar con: python manage.py shell < init_data.py
"""

from django.utils import timezone
from datetime import date, time, timedelta
from zonas_riego.models import Zona, Sensor
from programaciones.models import Programacion, HistorialRiego

print("🌱 Iniciando creación de datos de ejemplo...")

# Limpiar datos existentes (opcional)
# Zona.objects.all().delete()
# print("✓ Datos existentes eliminados")

# Crear Zonas
print("\n📍 Creando Zonas de Riego...")

zona1 = Zona.objects.create(
    nombre="Jardín Principal",
    descripcion="Jardín frontal con flores ornamentales",
    tipo_zona="jardin",
    area_m2=500.00,
    capacidad_agua_litros=25000.00,
    estado="activa",
    ubicacion="Frontal Norte",
    activa=True
)
print(f"  ✓ Creada: {zona1.nombre}")

zona2 = Zona.objects.create(
    nombre="Huerto Orgánico",
    descripcion="Huerto con vegetales y hortalizas",
    tipo_zona="huerto",
    area_m2=300.00,
    capacidad_agua_litros=15000.00,
    estado="activa",
    ubicacion="Lateral Este",
    activa=True
)
print(f"  ✓ Creada: {zona2.nombre}")

zona3 = Zona.objects.create(
    nombre="Césped Sur",
    descripcion="Área de césped para recreación",
    tipo_zona="cesped",
    area_m2=400.00,
    capacidad_agua_litros=20000.00,
    estado="activa",
    ubicacion="Parte Sur",
    activa=True
)
print(f"  ✓ Creada: {zona3.nombre}")

zona4 = Zona.objects.create(
    nombre="Cultivo Temporal",
    descripcion="Área para cultivos estacionales",
    tipo_zona="cultivo",
    area_m2=200.00,
    capacidad_agua_litros=10000.00,
    estado="mantenimiento",
    ubicacion="Oeste",
    activa=False
)
print(f"  ✓ Creada: {zona4.nombre}")

# Crear Sensores
print("\n🔧 Creando Sensores...")

sensor1 = Sensor.objects.create(
    zona=zona1,
    codigo="HUME-001",
    tipo_sensor="humedad",
    marca="DHT22",
    modelo="Pro",
    estado="operativo",
    valor_actual=45.50,
    unidad_medida="%",
    umbral_minimo=30.00,
    umbral_maximo=80.00,
    fecha_instalacion=date(2025, 1, 15),
    ultima_lectura=timezone.now(),
    activo=True
)
print(f"  ✓ Creado: {sensor1.codigo} en {sensor1.zona.nombre}")

sensor2 = Sensor.objects.create(
    zona=zona1,
    codigo="TEMP-001",
    tipo_sensor="temperatura",
    marca="DS18B20",
    modelo="Standard",
    estado="operativo",
    valor_actual=22.30,
    unidad_medida="°C",
    umbral_minimo=10.00,
    umbral_maximo=35.00,
    fecha_instalacion=date(2025, 1, 15),
    ultima_lectura=timezone.now(),
    activo=True
)
print(f"  ✓ Creado: {sensor2.codigo} en {sensor2.zona.nombre}")

sensor3 = Sensor.objects.create(
    zona=zona2,
    codigo="HUME-002",
    tipo_sensor="humedad",
    marca="DHT22",
    modelo="Pro",
    estado="operativo",
    valor_actual=55.00,
    unidad_medida="%",
    umbral_minimo=40.00,
    umbral_maximo=85.00,
    fecha_instalacion=date(2025, 2, 1),
    ultima_lectura=timezone.now(),
    activo=True
)
print(f"  ✓ Creado: {sensor3.codigo} en {sensor3.zona.nombre}")

sensor4 = Sensor.objects.create(
    zona=zona3,
    codigo="CAUD-001",
    tipo_sensor="caudal",
    marca="YF-S201",
    modelo="Flow",
    estado="operativo",
    valor_actual=8.50,
    unidad_medida="L/min",
    umbral_minimo=5.00,
    umbral_maximo=15.00,
    fecha_instalacion=date(2025, 3, 10),
    ultima_lectura=timezone.now(),
    activo=True
)
print(f"  ✓ Creado: {sensor4.codigo} en {sensor4.zona.nombre}")

sensor5 = Sensor.objects.create(
    zona=zona2,
    codigo="LLUV-001",
    tipo_sensor="lluvia",
    marca="RainSensor",
    modelo="V2",
    estado="operativo",
    valor_actual=0.00,
    unidad_medida="mm",
    umbral_minimo=0.00,
    umbral_maximo=50.00,
    fecha_instalacion=date(2025, 2, 15),
    ultima_lectura=timezone.now(),
    activo=True
)
print(f"  ✓ Creado: {sensor5.codigo} en {sensor5.zona.nombre}")

# Crear Programaciones
print("\n⏰ Creando Programaciones de Riego...")

prog1 = Programacion.objects.create(
    zona=zona1,
    nombre="Riego Mañana Jardín",
    descripcion="Riego diario matutino para el jardín principal",
    hora_inicio=time(7, 0),
    duracion_minutos=45,
    frecuencia="diaria",
    fecha_inicio=date(2025, 1, 1),
    estado="activa",
    caudal_litros_minuto=10.00,
    prioridad=7,
    activa=True
)
print(f"  ✓ Creada: {prog1.nombre}")

prog2 = Programacion.objects.create(
    zona=zona2,
    nombre="Riego Huerto Tarde",
    descripcion="Riego para el huerto orgánico en la tarde",
    hora_inicio=time(18, 30),
    duracion_minutos=60,
    frecuencia="diaria",
    fecha_inicio=date(2025, 1, 1),
    estado="activa",
    caudal_litros_minuto=8.00,
    prioridad=9,
    activa=True
)
print(f"  ✓ Creada: {prog2.nombre}")

prog3 = Programacion.objects.create(
    zona=zona3,
    nombre="Riego Césped Semanal",
    descripcion="Riego semanal del césped (Lunes, Miércoles, Viernes)",
    hora_inicio=time(6, 30),
    duracion_minutos=30,
    frecuencia="semanal",
    dias_semana=["lunes", "miercoles", "viernes"],
    fecha_inicio=date(2025, 1, 1),
    estado="activa",
    caudal_litros_minuto=12.00,
    prioridad=5,
    activa=True
)
print(f"  ✓ Creada: {prog3.nombre}")

prog4 = Programacion.objects.create(
    zona=zona1,
    nombre="Riego Nocturno Jardín",
    descripcion="Riego adicional nocturno en verano",
    hora_inicio=time(22, 0),
    duracion_minutos=30,
    frecuencia="semanal",
    dias_semana=["martes", "jueves", "sabado"],
    fecha_inicio=date(2025, 11, 1),
    fecha_fin=date(2026, 3, 31),
    estado="activa",
    caudal_litros_minuto=9.00,
    prioridad=4,
    activa=True
)
print(f"  ✓ Creada: {prog4.nombre}")

# Crear Historial de Riegos
print("\n📊 Creando Historial de Riegos...")

# Historial 1 - Exitoso
historial1 = HistorialRiego.objects.create(
    programacion=prog1,
    zona=zona1,
    fecha_ejecucion=timezone.now() - timedelta(days=1, hours=17),
    hora_inicio_real=time(7, 0),
    hora_fin_real=time(7, 45),
    duracion_real_minutos=45,
    caudal_real_litros_minuto=10.00,
    consumo_total_litros=450.00,
    resultado="exitoso",
    observaciones="Riego completado sin incidencias",
    temperatura_ambiente=22.50,
    humedad_suelo_antes=35.00,
    humedad_suelo_despues=75.00
)
print(f"  ✓ Creado historial: {historial1.zona.nombre} - {historial1.resultado}")

# Historial 2 - Exitoso
historial2 = HistorialRiego.objects.create(
    programacion=prog2,
    zona=zona2,
    fecha_ejecucion=timezone.now() - timedelta(days=1, hours=5, minutes=30),
    hora_inicio_real=time(18, 30),
    hora_fin_real=time(19, 30),
    duracion_real_minutos=60,
    caudal_real_litros_minuto=8.00,
    consumo_total_litros=480.00,
    resultado="exitoso",
    observaciones="Riego óptimo, buena absorción",
    temperatura_ambiente=25.00,
    humedad_suelo_antes=42.00,
    humedad_suelo_despues=82.00
)
print(f"  ✓ Creado historial: {historial2.zona.nombre} - {historial2.resultado}")

# Historial 3 - Parcial
historial3 = HistorialRiego.objects.create(
    programacion=prog3,
    zona=zona3,
    fecha_ejecucion=timezone.now() - timedelta(days=2, hours=17, minutes=30),
    hora_inicio_real=time(6, 30),
    hora_fin_real=time(6, 50),
    duracion_real_minutos=20,
    caudal_real_litros_minuto=12.00,
    consumo_total_litros=240.00,
    resultado="parcial",
    observaciones="Riego interrumpido por baja presión de agua",
    temperatura_ambiente=20.00,
    humedad_suelo_antes=38.00,
    humedad_suelo_despues=55.00
)
print(f"  ✓ Creado historial: {historial3.zona.nombre} - {historial3.resultado}")

# Historial 4 - Exitoso (hoy)
historial4 = HistorialRiego.objects.create(
    programacion=prog1,
    zona=zona1,
    fecha_ejecucion=timezone.now() - timedelta(hours=4),
    hora_inicio_real=time(7, 0),
    hora_fin_real=time(7, 45),
    duracion_real_minutos=45,
    caudal_real_litros_minuto=10.00,
    consumo_total_litros=450.00,
    resultado="exitoso",
    observaciones="Riego de hoy completado exitosamente",
    temperatura_ambiente=21.00,
    humedad_suelo_antes=40.00,
    humedad_suelo_despues=78.00
)
print(f"  ✓ Creado historial: {historial4.zona.nombre} - {historial4.resultado}")

print("\n✅ ¡Datos de ejemplo creados exitosamente!")
print("\n📈 Resumen:")
print(f"  - Zonas creadas: {Zona.objects.count()}")
print(f"  - Sensores creados: {Sensor.objects.count()}")
print(f"  - Programaciones creadas: {Programacion.objects.count()}")
print(f"  - Historiales creados: {HistorialRiego.objects.count()}")
print("\n🌐 Puedes acceder a:")
print("  - Swagger: http://localhost:8000/swagger/")
print("  - Admin: http://localhost:8000/admin/")
print("  - API Zonas: http://localhost:8000/api/zonas/")
print("  - API Programaciones: http://localhost:8000/api/programaciones/")
