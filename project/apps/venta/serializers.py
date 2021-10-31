from rest_framework_json_api import serializers

from venta.models import Product, OrderDetail, Order
from venta.services import service_usd


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
        fields = ('date_time', 'total_arg', 'total_usd', 'order_detail')
        extra_kwargs = {
            'order_detail': {'required': False},
        }

    total_arg = serializers.SerializerMethodField(method_name='get_total_arg')
    total_usd = serializers.SerializerMethodField(method_name='get_total_usd')

    included_serializers = {
        'order_detail': OrderDetailSerializer
    }

    def get_total_arg(self, order):
        total = 0
        for orderdetail in order.order_detail.all():
            total = total + orderdetail.product.price * orderdetail.cuantity
        return total

    def get_total_usd(self, order):
        dolar_blue = service_usd()
        total_usd = self.get_total_arg(order) / dolar_blue

        return round(total_usd, 2)

