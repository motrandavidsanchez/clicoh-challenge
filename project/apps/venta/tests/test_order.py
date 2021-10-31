import pytest
from venta.tests.fixture import create_order, create_order_detail, create_products, create_user
from venta.utils import get, post, delete


@pytest.mark.django_db
def test_get_orders(create_order, create_order_detail):
    usuario = create_user(username='david')

    response = get('/api/v1/order/', user_logged=usuario)

    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_order(create_order, create_order_detail):
    order_one, order_two, order_three = create_order
    usuario = create_user(username='david')

    response = get(f'/api/v1/order/{order_one.id}/', user_logged=usuario)

    assert response.status_code == 200

    data = response.json()['data']

    assert data['attributes']['date_time'] == '2021-10-30T10:30:00-03:00'
    assert data['attributes']['total_arg'] == 420.0
    assert data['attributes']['total_usd'] == 2.13


@pytest.mark.django_db
def test_create_order(create_order):
    usuario = create_user(username='david')

    data = {
        'data': {
            'type': 'Order',
            'attributes': {
                'date_time': '2021-10-30 12:44',
            }
        }
    }

    response = post(f'/api/v1/order/', data=data, user_logged=usuario)

    assert response.status_code == 201

    data = response.json()['data']

    assert data['attributes']['date_time'] == '2021-10-30T12:44:00-03:00'


@pytest.mark.django_db
def test_delete_order(create_order):
    order_one, order_two, order_three = create_order
    usuario = create_user(username='david')

    response = delete(f'/api/v1/order/{order_one.id}/', user_logged=usuario)

    assert response.status_code == 204
