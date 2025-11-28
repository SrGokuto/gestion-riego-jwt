"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Configuración de Swagger/OpenAPI Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="🌱 API de Gestión de Riego Automatizado",
        default_version='v1',
        description="""
        API REST completa para el sistema de gestión de riego automatizado.
        
        ## 🎯 Características principales:
        - **Zonas de Riego**: Gestión completa de zonas de riego
        - **Programaciones**: Configuración de horarios y frecuencias de riego
        - **Sensores**: Monitoreo de humedad y temperatura
        - **Consumo de Agua**: Control y seguimiento del consumo de agua
        - **Estadísticas**: Endpoints de análisis y reportes
        
        ## 📦 Aplicaciones:
        
        ### 🌳 Zonas de Riego (`/api/zonas/`)
        - Gestión de zonas de riego
        - Tipos: jardín, huerto, césped, cultivo, ornamental
        - Estados: activa, inactiva, mantenimiento
        - Filtros por tipo, estado, área y capacidad
        - Estadísticas y resúmenes detallados
        
        ### 📅 Programaciones (`/api/programaciones/`)
        - Programación de riegos automáticos
        - Frecuencias: diaria, semanal, quincenal, mensual, personalizada
        - Sistema de prioridades (1-10)
        - Control de vigencia y ejecución
        - Simulación de riegos
        
        ### 📊 Sensores (`/api/sensores/` y `/api/lecturas/`)
        - Gestión de sensores de humedad y temperatura
        - Registro de lecturas en tiempo real
        - Consulta de histórico de lecturas
        - Filtros por sensor, fecha y tipo
        
        ### 💧 Consumo de Agua (`/api/medidores/` y `/api/consumos/`)
        - Gestión de medidores de agua
        - Registro de consumo diario (m³)
        - Seguimiento por medidor y fecha
        - Análisis de consumo histórico
        
        ## 🔍 Filtrado y Búsqueda:
        Todos los endpoints de listado soportan filtrado avanzado mediante query parameters.
        
        ## 📄 Paginación:
        Los resultados están paginados (10 items por página por defecto).
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@riego.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Accounts
    path('auth/', include('accounts.urls')),

    # Admin
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/', include('zonas_riego.urls')),
    path('api/', include('programaciones.urls')),
    path('api/', include('sensores.urls')),
    path('api/', include('consumo_agua.urls')),
    
    # Documentación Swagger/OpenAPI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-root'),
]

