from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet

router = DefaultRouter()
router.register('cart', CartItemViewSet, basename='cart')

urlpatterns = router.urls
