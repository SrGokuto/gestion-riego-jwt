from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramacionViewSet

router = DefaultRouter()
router.register(r'programaciones', ProgramacionViewSet, basename='programacion')

app_name = 'programaciones'

urlpatterns = [
    path('', include(router.urls)),
]
