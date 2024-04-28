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


def get_route(api_key, vehicle, start_lat, start_lon, end_lat, end_lon):
    url = f"https://graphhopper.com/api/1/route?point={start_lat},{start_lon}&point={end_lat},{end_lon}&vehicle={vehicle}&locale=en&key={api_key}"
    print(url)
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

def get_info(api_key, vehicle, start_lat, start_lon, end_lat, end_lon):
    # Get the route
    route_data = get_route(api_key, vehicle, start_lat, start_lon, end_lat, end_lon)
    if route_data is not None:
        # Parse the route coordinates
        coordinates = parse_route_coordinates(route_data)
        sec = int(route_data["paths"][0]["time"] / 1000 % 60)
        min = int(route_data["paths"][0]["time"] / 1000 / 60 % 60)
        hr = int(route_data["paths"][0]["time"] / 1000 / 60 / 60 % 24)
        days = int(route_data["paths"][0]["time"] / 1000 / 60 / 60 / 24)
        if days > 0:
            total_time = str(days)+("days " if days > 0 else "day ") + str(hr).zfill(2)+"h "+str(min).zfill(2) + "min " + str(sec).zfill(2) + "sec"
        elif hr > 0:
            total_time = str(hr) + "h " + str(min).zfill(2) + "min " + str(sec).zfill(2) + "sec"
        elif min > 0:
            total_time = str(min) + "min " + str(sec).zfill(2) + "sec"
        else:
            total_time = str(sec) + "sec"

        total_distance = route_data["paths"][0]["distance"]
        if total_distance > 1000:
            total_distance_km = str(round(total_distance/1000, 2)) + " Km"
        else:
            total_distance_km = str(int(total_distance)) + " m"
        total_distance_miles = str(round(total_distance / 1000 / 1.61, 2)) + " miles"

        instructions = route_data["paths"][0]["instructions"]
        str_instructions = []
        for each in range(len(route_data["paths"][0]["instructions"])):
            path = route_data["paths"][0]["instructions"][each]["text"]
            distance = route_data["paths"][0]["instructions"][each]["distance"]
            sec = int(route_data["paths"][0]["instructions"][each]["time"] / 1000 % 60)
            min = int(route_data["paths"][0]["instructions"][each]["time"]/ 1000 / 60 % 60)
            hr = int(route_data["paths"][0]["instructions"][each]["time"] / 1000 / 60 / 60)
            if hr > 0:
                time = str(hr) + "h " + str(min).zfill(2) + "min " + str(sec).zfill(2) + "sec"
            elif min > 0:
                time = str(min) + "min " + str(sec).zfill(2) + "sec"
            else:
                time = str(sec) + "sec"

            if distance > 1000:
                distance_km = str(round(distance/1000, 2)) + " Km"
            else:
                distance_km = str(int(distance)) + " m"

            distance_miles = str(round(distance / 1000 / 1.61, 2)) + " miles"
            current_instruction = "{0} during {1} ( {2} / {3} )".format(path, time, distance_km,
                                                              distance_miles)
            str_instructions.append(current_instruction)
        return coordinates, total_time, (total_distance_km, total_distance_miles), str_instructions
    return None, None, (None, None), None