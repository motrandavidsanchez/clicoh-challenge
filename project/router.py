from rest_framework.routers import DefaultRouter

from venta.apis import ProductViewSet, OrderDetailViewSet

router = DefaultRouter()

router.register('product', ProductViewSet, basename='product')
router.register('order-detail', OrderDetailViewSet, basename='order-detail')
