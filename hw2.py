from maps_api.geocoder import get_ll_spn
from maps_api.geocoder import geocode

address = input()
ll, spn = get_ll_spn(address)
json_response = geocode(ll, {'kind': 'district'})

r = json_response['metaDataProperty']['GeocoderMetaData']['Address']['Components'][5]['name']

print(r)