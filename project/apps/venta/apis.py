from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from venta.models import Product, OrderDetail, Order
from venta.serializers import ProductSerializer, OrderDetailSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        # Controla Stock
        if product.stock <= 0:
            raise ValidationError('No hay suficiente stock.')

        # Controla cantidad
        if serializer.validated_data['cuantity'] <= 0:
            raise ValidationError('La cantidad debe ser mayor a cero.')

        # Controla que el producto no se repita
        order_detail = OrderDetail.objects.filter(order=serializer.validated_data['order'].id, product=product.id)

        if order_detail.exists:
            raise ValidationError('El producto ya se encuentra en la orden.')


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
