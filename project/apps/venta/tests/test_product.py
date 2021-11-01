import pytest

from venta.tests.fixture import create_products, create_user
from venta.utils import post, get, patch, delete


@pytest.mark.django_db
def test_get_products(create_products):
    usuario = create_user(username='david')

    response = get('/api/v1/product/', user_logged=usuario)

    assert response.status_code == 200

    data = response.json()['data']

    assert data[0]['attributes']['name'] == 'Sombrero negro'
    assert data[1]['attributes']['name'] == 'Zapatos Blancos'
    assert data[2]['attributes']['name'] == 'Remeras'
    assert data[3]['attributes']['name'] == 'Cartera'


@pytest.mark.django_db
def test_create_product():
    usuario = create_user(username='david')

    data = {
        'data': {
            'type': 'Product',
            'attributes': {
                'name': 'Gorra',
                'price': 79.9,
                'stock': 10,
            }
        }
    }

    response = post('/api/v1/product', data=data, user_logged=usuario)

    assert response.status_code == 201

    data = response.json()['data']

    assert data['attributes']['name'] == 'Gorra'
    assert data['attributes']['price'] == 79.9
    assert data['attributes']['stock'] == 10


@pytest.mark.django_db
def test_update_product(create_products):
    product_one, product_two, product_three, product_four = create_products
    usuario = create_user(username='david')

    data = {
        'data': {
            'type': 'Product',
            'id': product_two.id,
            'attributes': {
                'price': 385,
            }
        }
    }

    response = patch(f'/api/v1/product/{product_two.id}/', data=data, user_logged=usuario)

    assert response.status_code == 200

    data = response.json()['data']

    assert data['attributes']['price'] == 385


@pytest.mark.django_db
def test_delete_product(create_products):
    product_one, product_two, product_three, product_four = create_products
    usuario = create_user(username='david')

    response = delete(f'/api/v1/product/{product_two.id}/', user_logged=usuario)

    assert response.status_code == 204
