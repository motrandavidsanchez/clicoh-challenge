import pytest
from django.contrib.auth import get_user_model

from venta.models import Product

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
