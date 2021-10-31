import pytest
from venta.tests.fixture import create_products, create_order, create_order_detail, create_user
from venta.utils import get, post, patch, delete


@pytest.mark.django_db
def test_get_order_detail(create_order_detail):
    usuario = create_user(username='david')

    response = get('/api/v1/order-detail/', user_logged=usuario)

    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_order_detail(create_order_detail, create_order, create_products):
    order_detail_one, order_detail_two, order_detail_three, order_detail_four = create_order_detail
    order_one, order_two, order_three = create_order
    product_one, product_two, product_three = create_products

    usuario = create_user(username='david')

    response = get(f'/api/v1/order-detail/{order_detail_one.id}/', user_logged=usuario)

    assert response.status_code == 200

    data = response.json()['data']

    assert data['relationships']['order']['data']['id'] == str(order_one.id)
    assert data['relationships']['product']['data']['id'] == str(product_one.id)


@pytest.mark.django_db
def test_create_order_detail(create_order, create_products):
    order_one, order_two, order_three = create_order
    product_one, product_two, product_three = create_products

    usuario = create_user(username='david')

    data = {
        'data': {
            'type': 'OrderDetail',
            'attributes': {
                'cuantity': 1,
            },
            'relationships': {
                'order': {
                    'data': {
                        'type': 'Order',
                        'id': order_three.id
                    }
                },
                'product': {
                    'data': {
                        'type': 'Product',
                        'id': product_two.id
                    }
                }
            }
        }
    }

    response = post('/api/v1/order-detail/', data=data, user_logged=usuario)

    assert response.status_code == 201


@pytest.mark.django_db
def test_update_order_detail(create_order_detail):
    order_detail_one, order_detail_two, order_detail_three, order_detail_four = create_order_detail
    usuario = create_user(username='david')

    assert order_detail_four.cuantity == 2

    data = {
        'data': {
            'type': 'OrderDetail',
            'id': order_detail_four.id,
            'attributes': {
                'cuantity': 3,
            }
        }
    }

    response = patch(f'/api/v1/order-detail/{order_detail_four.id}/', data=data, user_logged=usuario)

    assert response.status_code == 200

    data = response.json()['data']

    assert data['attributes']['cuantity'] == 3


@pytest.mark.django_db
def test_delete_order_detail(create_order_detail):
    order_detail_one, order_detail_two, order_detail_three, order_detail_four = create_order_detail
    usuario = create_user(username='david')

    response = delete(F'/api/v1/order-detail/{order_detail_one.id}', user_logged=usuario)

    assert response.status_code == 204
