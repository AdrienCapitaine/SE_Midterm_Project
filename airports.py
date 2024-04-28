import urllib.parse
import requests

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    float lon1, float lat1, float lon2, float lat2 -> float distance

    Calculates the distance in kilometers between two points 
    on the earth.
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
    str destinationCity, tpl(float latitude,float longitude)  coords-> list[dict] airports
    
    This function returns a list dictionnaries describing airports that are affiliated to the destination city as well as within 50 km of the input coordinates.
    """
    key = "LeLHVfX2J+40J2TpuXen7A==JckrqmRp99HGwL2a"

    url = "https://api.api-ninjas.com"
    uri_nearest_airport = "/v1/airports"
    radius = 50 # 0.5 mile radius around nodes 

    result = []
    res = [1]
    airports =[]
    i = 0

    while True:
        req = url + uri_nearest_airport + "?"+ urllib.parse.urlencode({"city" : destinationCity, "offset" : i})
        res = requests.get(req,headers={'X-Api-Key': key}).json()
        airports += res
        if len(res)==0:
            break
        i+= len(res)

    #print(len(airports))
    if len(airports) != 0:
        try:
            a = airports[0]["latitude"]
        except:
            raise ValueError("Api key is invalid or has expired. Please request a new one.")
    #print("End of request")
    for airport in airports:
        distance = haversine(coords[0],coords[1], float(airport["latitude"]), float(airport["longitude"]))

        
        if distance <= radius:
            print(airport["name"], '/',airport["icao"],'/',distance, '/',airport["latitude"],'/', airport["longitude"] , '/',airport["city"] , '/', airport["country"], '/', distance)
            airport["distance"] = distance
            result.append(airport)

    #print(result)
    return result

# Example
#get_airports("London", (51.5073509,-0.1277583)) # gets airports in London that are within 50 km of the input coordinates
#get_airports("Moscow", (55.7558, 37.6176)) # gets airports in Moscow that are within 50 km of the input coordinates