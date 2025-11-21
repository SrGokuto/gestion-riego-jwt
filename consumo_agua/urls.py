from rest_framework.routers import DefaultRouter
from .views import MedidorViewSet, ConsumoViewSet

router = DefaultRouter()
router.register('medidores', MedidorViewSet)
router.register('consumos', ConsumoViewSet)

urlpatterns = router.urls
