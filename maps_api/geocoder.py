from io import BytesIO

import requests
from PIL import Image

API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"


def geocode(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if response:
        json_response = response.json()
    else:
        raise RuntimeError(f'''Ошибка выполнения запроса: {response.url}\nHTTP статус:{response.status_code}({response.reason})''')

    return json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]


def get_ll_spn(address):
    toponym = geocode(address)
    if not toponym:
        return None, None

    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    ll = ",".join([toponym_longitude, toponym_lattitude])

    envelope = toponym['boundedBy']['Envelope']
    l, b = envelope['lowerCorner'].split(' ')
    r, t = envelope['upperCorner'].split(' ')
    dx, dy = abs(float(l) - float(r)) / 2, abs(float(t) - float(b)) / 2
    spn = ','.join([str(dx), str(dy)])

    return ll, spn


def get_nearest_object(ll, spn):
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": "map",
        'pt': f'{ll},pm2rdm'
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    return response


def show_map(response):
    Image.open(BytesIO(response.content)).show()