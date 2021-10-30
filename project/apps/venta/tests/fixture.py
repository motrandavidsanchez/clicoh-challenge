import pytest
from django.contrib.auth import get_user_model

from venta.models import Product, Order, OrderDetail

User = get_user_model()


def create_user(username, first_name='Admin', last_name='Root', email=None, is_superuser=False, is_staff=False):
    user, created = User.objects.get_or_create(
        username=username,
        email='{}@root.com'.format(username) if email is None else email,
        defaults=dict(
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser,
            is_staff=is_staff,
        )
    )

    user.set_password('password')
    user.save()

    return user


@pytest.fixture
def create_products():

    product_one, _ = Product.objects.get_or_create(
        name='Sombrero negro',
        price=50.0,
        stock=5
    )

    product_two, _ = Product.objects.get_or_create(
        name='Zapatos Blancos',
        price=370.0,
        stock=5
    )

    product_three, _ = Product.objects.get_or_create(
        name='Remeras',
        price=167.0,
        stock=5
    )

    return product_one, product_two, product_three


@pytest.fixture()
def create_order():

    order_one, _ = Order.objects.get_or_create(
        date_time='2021-10-30 10:30'
    )

    order_two, _ = Order.objects.get_or_create(
        date_time='2021-9-30 14:35'
    )

    order_three, _ = Order.objects.get_or_create(
        date_time='2021-10-25 18:16'
    )

    return order_one, order_two, order_three


@pytest.fixture()
def create_order_detail(create_products, create_order):
    product_one, product_two, product_three = create_products
    order_one, order_two, order_three = create_order

    order_detail_one, _ = OrderDetail.objects.get_or_create(
        order=order_one,
        product=product_one,
        cuantity=1
    )

    order_detail_two, _ = OrderDetail.objects.get_or_create(
        order=order_one,
        product=product_two,
        cuantity=1
    )

    order_detail_three, _ = OrderDetail.objects.get_or_create(
        order=order_two,
        product=product_three,
        cuantity=2
    )

    order_detail_four, _ = OrderDetail.objects.get_or_create(
        order=order_three,
        product=product_one,
        cuantity=2
    )

    return order_detail_one, order_detail_two, order_detail_three, order_detail_four
