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
        fields = ('date_time', 'total', 'order_detail')
        extra_kwargs = {
            'order_detail': {'required': False},
        }

    total = serializers.SerializerMethodField(method_name='get_total')

    included_serializers = {
        'order_detail': OrderDetailSerializer
    }

    def get_total(self, order):
        total = 0
        for orderdetail in order.order_detail.all():
            total = total + orderdetail.product.price * orderdetail.cuantity
        return total
