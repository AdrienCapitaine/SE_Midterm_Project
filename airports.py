import urllib.parse
import requests

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculates the distance in kilometers between two points 
    on the earth 
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r


def get_airports(destinationCity,coords):
    """
    str,tpl[latitude,longitude] -> list[dict] (airports)
    """
    key = "LeLHVfX2J+40J2TpuXen7A==JckrqmRp99HGwL2a"

    url = "https://api.api-ninjas.com"
    uri_nearest_airport = "/v1/airports"
    radius = 50 # 0.5 mile radius around nodes 
    
    airports = []
    res = [1]
    airports =[]
    i = 0

    while len(res)!=0:
        req = url + uri_nearest_airport + "?"+ urllib.parse.urlencode({"city" : destinationCity, "offset" : i})
        res = requests.get(req,headers={'X-Api-Key': key}).json()
        airports += res
        i+=1 

    print(len(airports))
    
    for airport in airports:
        distance = haversine(coords[0],coords[1], float(airport["latitude"]), float(airport["longitude"]))
        #print(airport["name"], airport["icao"],distance, airport["latitude"], airport["longitude"] , airport["city"] , '/', airport["country"])
        
        if distance <= radius:
            print(airport["name"], '/',airport["icao"],'/',distance, '/',airport["latitude"],'/', airport["longitude"] , '/',airport["city"] , '/', airport["country"], '/', distance)
            airport["distance"] = distance
            airports.append(airport)

        
    return airports

#haversine(40.7, -74, 48.864716, 2.34)
#get_airports("London", (51.5073509,-0.1277583)) # gets airports in London that are within 50 km of the input coordinates

#get_airports("Moscow", (55.7558, 37.6176)) # gets airports in Moscow that are within 50 km of the input coordinates