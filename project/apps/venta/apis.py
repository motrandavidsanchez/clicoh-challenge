from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters

from venta.models import Product, OrderDetail, Order
from venta.serializers import ProductSerializer, OrderDetailSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_fields = ['name']
    permission_classes = (IsAuthenticated,)


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['product__name']
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        cuantity = serializer.validated_data['cuantity']

        # Controla cantidad
        if cuantity <= 0:
            raise ValidationError('La cantidad debe ser mayor a cero.')

        # Controla que el producto no se repita
        order_detail = OrderDetail.objects.filter(order=serializer.validated_data['order'].id, product=product.id)
        if order_detail.exists():
            raise ValidationError('El producto ya se encuentra en la orden.')

        # Controla y Resta Stock de producto
        if product.stock <= 0:
            raise ValidationError('No hay suficiente stock.')
        else:
            product.stock = product.stock - cuantity
            product.save()

        return serializer.save()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('order_detail', 'order_detail__product')
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        for orderdetail in instance.order_detail.all():
            product = orderdetail.product
            product.stock = product.stock + orderdetail.cuantity
            product.save()

        return instance
