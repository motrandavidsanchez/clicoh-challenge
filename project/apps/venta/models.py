import datetime

from django.db import models


class Product(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(blank=True, null=True)
    stock = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    date_time = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return str(self.date_time)


class OrderDetail(models.Model):
    class Meta:
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Orders Detail'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_detail')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cuantity = models.IntegerField()

    def __str__(self):
        return f'{self.order} -> {self.product}'
