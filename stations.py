#!/usr/bin/env python3
import urllib.parse
import json
import requests


#output format : https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/nearest/#json-output-format
def get_stations(coords):
    """
    list[tpl (float latitude, float longitude)] coords -> list[dict] stations

    Retrieves stations within a 0.5 mile radius of provided coordinates
    
    """
    key =  "hqJtmjmuvQcBmc8IwyorOww2FzXJIrXcGfqTchBf" #apikey
    url = "https://developer.nrel.gov"
    uri_nearest_station = "/api/alt-fuel-stations/v1/nearest.json"
    range = 0.5 # 0.5 mile radius around nodes 
    
    stations = []

    for coord in coords:
        latitude = coord[0]
        longitude = coord[1]
        res = requests.get(url + uri_nearest_station + "?" + urllib.parse.urlencode({"api_key":key, "latitude": latitude, "longitude": longitude, "radius" : 5})).json()
        
        for station in res["fuel_stations"]:
            stations.append({"latitude" : station["latitude"], "longitude" : station["longitude"], "name" : station["station_name"], "street_address" : station["street_address"], "city" : station["city"],  "fuel_type_code" : station["fuel_type_code"]})
    
    #for el in stations:
      #  print(el)
        
    return stations
    

#get_stations([(40.7, -74)])#new york
#get_stations([( 48.864716, 2.34)]) #"paris"
