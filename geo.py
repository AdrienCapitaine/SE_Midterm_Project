import urllib
import requests
from polyline import polyline

def geocoding (location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1",
    "key":key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    if json_status == 200 and len(json_data["hits"]) !=0:
        json_data = requests.get(url).json()
        lat=(json_data["hits"][0]["point"]["lat"])
        lng=(json_data["hits"][0]["point"]["lng"])
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country=""

        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state=""

        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) !=0:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)
    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status != 200:
            print("Geocode API status: " + str(json_status) + "\nError message: " + json_data["message"])
    return json_status,lat,lng,new_loc


def get_route(api_key, start_lat, start_lon, end_lat, end_lon):
    url = f"https://graphhopper.com/api/1/route?point={start_lat},{start_lon}&point={end_lat},{end_lon}&vehicle=car&locale=en&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_route_coordinates(route_data):
    if route_data is not None:
        points = route_data['paths'][0]['points']
        decoded_points = polyline.decode(points)
        points = [[point[0], point[1]] for point in decoded_points]
        return points
    return None

def get_coordinate(api_key, start_lat, start_lon, end_lat, end_lon):
    # Get the route
    route_data = get_route(api_key, start_lat, start_lon, end_lat, end_lon)

    # Parse the route coordinates
    coordinates = parse_route_coordinates(route_data)
    return coordinates


api_key = "436b1d6d-1167-4c86-9093-00fa35072e7f"

o1 = geocoding("Paris", api_key)
o2 = geocoding("Rennes", api_key)
print(o1)
print(o2)
print(get_coordinate(api_key, o1[1], o1[2], o2[1], o2[2]))