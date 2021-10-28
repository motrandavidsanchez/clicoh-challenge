from rest_framework.routers import DefaultRouter

from venta.apis import ProductViewSet

router = DefaultRouter()

router.register('product', ProductViewSet, basename='product')
