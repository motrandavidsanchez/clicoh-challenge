from django.contrib import admin

# Register your models here.
from venta.models import Product, Order, OrderDetail


@admin.register(Product)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'price')
    search_fields = ('name',)


class OrderDetailStackedInline(admin.StackedInline):
    model = OrderDetail
    extra = 0
    autocomplete_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('date_time',)
    inlines = (OrderDetailStackedInline,)



