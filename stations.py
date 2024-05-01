#!/usr/bin/env python3
import urllib.parse
import json
import requests


#output format : https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/nearest/#json-output-format
def get_stations(coords):
       """
    Retrieves information about fuel stations within a 0.5 mile radius of provided coordinates.

    Parameters:
    - coords (list[tuple(float, float)]): A list of latitude and longitude coordinates.

    Returns:
    - stations (list[dict]): A list of dictionaries containing information about fuel stations found within the specified radius.
        Each dictionary includes the following keys:
        - 'latitude' (float): Latitude coordinate of the fuel station.
        - 'longitude' (float): Longitude coordinate of the fuel station.
        - 'name' (str): Name of the fuel station.
        - 'street_address' (str): Street address of the fuel station.
        - 'city' (str): City where the fuel station is located.
        - 'fuel_type_code' (str): Code representing the type of fuel available at the station.

    Dependencies:
    - requests: Used to perform HTTP requests.
    - urllib.parse: Used to encode parameters for the API request.

    API Key:
    - The function requires an API key for authentication with the National Renewable Energy Laboratory (NREL) API. 
      The API key should be provided in the function code.

    API Endpoint:
    - The function utilizes the NREL API endpoint '/api/alt-fuel-stations/v1/nearest.json' to fetch information about nearby fuel stations.

    Radius:
    - The function searches for fuel stations within a 0.5-mile radius of each provided coordinate.

    """
    key =  "hqJtmjmuvQcBmc8IwyorOww2FzXJIrXcGfqTchBf" #apikey
    url = "https://developer.nrel.gov"
    uri_nearest_station = "/api/alt-fuel-stations/v1/nearest.json"
    range = 0.5 # 0.5 mile radius around nodes 
    
    stations = []

    for coord in coords:
        latitude = coord[0]
        longitude = coord[1]
        res = requests.get(url + uri_nearest_station + "?" + urllib.parse.urlencode({"api_key":key, "latitude": latitude, "longitude": longitude, "radius" : 1})).json()
        
        for station in res["fuel_stations"]:
            stations.append({"latitude" : station["latitude"], "longitude" : station["longitude"], "name" : station["station_name"], "street_address" : station["street_address"], "city" : station["city"],  "fuel_type_code" : station["fuel_type_code"]})
    

    return stations
    

#get_stations([(40.7, -74)])#new york Example use case

