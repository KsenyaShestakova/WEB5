from maps_api.geocoder import get_ll_spn, find_nearest_organization, show_map
import math


ll, spn = get_ll_spn("Пермь, Докучаева 40В")
organization = find_nearest_organization(ll, spn, "аптека")
org_ll = ",".join(map(str, organization["geometry"]["coordinates"]))
spn = f'{abs(float(ll.split(",")[0]) - organization["geometry"]["coordinates"][0]) * 2},' \
      f'{abs(float(ll.split(",")[1]) - organization["geometry"]["coordinates"][1]) * 2}'
show_map(ll, spn, add_params={"pt": f"{ll},pm2rdm~{org_ll},pm2gnm"})

name = organization["properties"]["CompanyMetaData"]["name"]
address = organization["properties"]["CompanyMetaData"]["address"]
work_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]

degree_to_meters_factors = 111300

a_lon, a_lat = map(float, ll.split(","))
b_lon, b_lat = map(float, org_ll.split(","))
radians_l = math.radians((a_lat + b_lat) / 2)
lat_lon_factor = math.cos(radians_l)

dx = abs(a_lon - b_lon) * degree_to_meters_factors * lat_lon_factor
dy = abs(a_lat - b_lat) * degree_to_meters_factors

distance = math.sqrt(dx * dx + dy * dy)
print(name, address, work_time, str(distance) + " м.", sep='\n')