from rest_framework_json_api import serializers

from venta.models import Product, OrderDetail, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

    included_serializers = {
        'product': ProductSerializer
    }


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('date_time', 'order_detail')

    included_serializers = {
        'order_detail': OrderDetailSerializer
    }
