import requests
from django.http import HttpResponse


def service_usd():
    response = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')

    if response.status_code == 200:
        valoraciones = response.json()
        dolar_blue = valoraciones[1]['casa']['venta'].replace(',', '.')
        return float(dolar_blue)
    else:
        return HttpResponse("{'status': 'fail', 'msg': 'Error al consultar Dolarsi'}", content_type='aplication/json')
