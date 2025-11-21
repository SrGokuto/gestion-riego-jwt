from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ZonaViewSet

router = DefaultRouter()
router.register(r'zonas', ZonaViewSet, basename='zona')

app_name = 'zonas_riego'

urlpatterns = [
    path('', include(router.urls)),
]
