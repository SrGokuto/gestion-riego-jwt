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

# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API de Gestión de Riego Automatizado",
        default_version='v1',
        description="""
        API REST para el sistema de gestión de riego automatizado.
        
        ## Características principales:
        - **Zonas de Riego**: Gestión completa de zonas de riego con sensores
        - **Programaciones**: Configuración de horarios y frecuencias de riego
        - **Historial**: Registro y análisis de riegos ejecutados
        - **Estadísticas**: Endpoints de análisis y reportes
        
        ## Aplicaciones:
        ### Zonas de Riego
        - Gestión de zonas y sensores
        - Filtros por tipo, estado y área
        - Estadísticas y resúmenes
        
        ### Programaciones
        - Programación de riegos automáticos
        - Gestión de horarios y frecuencias
        - Historial de ejecuciones
        - Análisis de consumo de agua
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@riego.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # APIs
    path('api/', include('zonas_riego.urls')),
    path('api/', include('programaciones.urls')),
    
    # Documentación Swagger/OpenAPI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-root'),
]
