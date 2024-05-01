import urllib.parse
import requests

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculates the distance in kilometers between two points on the Earth using the Haversine formula.

    Parameters:
    - lon1 (float): Longitude of the first point in degrees.
    - lat1 (float): Latitude of the first point in degrees.
    - lon2 (float): Longitude of the second point in degrees.
    - lat2 (float): Latitude of the second point in degrees.

    Returns:
    - distance (float): The distance between the two points in kilometers.

    Formula:
    - The function applies the Haversine formula to calculate the distance between two points on a sphere.
    - The formula takes into account the curvature of the Earth's surface.

    Dependencies:
    - math.radians: Converts angles from degrees to radians.
    - math.sin: Computes the sine of an angle.
    - math.cos: Computes the cosine of an angle.
    - math.sqrt: Computes the square root of a number.
    - math.asin: Computes the arcsine of a value.

    Constants:
    - r (float): Radius of the Earth in kilometers. The function assumes a spherical Earth with a radius of 6371 kilometers.

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
    Retrieves information about airports affiliated with the destination city and within 50 kilometers of the input coordinates.

    Parameters:
    - destinationCity (str): The name of the destination city.
    - coords (tuple(float, float)): Latitude and longitude coordinates of the location.

    Returns:
    - airports (list[dict]): A list of dictionaries containing information about airports that meet the specified criteria.
        Each dictionary includes various details about the airport, such as name, ICAO code, latitude, longitude, city, country, and distance from the input coordinates.

    Dependencies:
    - requests: Used to perform HTTP requests.
    - urllib.parse: Used to encode parameters for the API request.
    - haversine: A function to calculate the distance between two points on the Earth's surface.

    API Key:
    - The function requires an API key for authentication with the API-Ninjas API. 
      The API key should be provided in the function code.

    API Endpoint:
    - The function utilizes the API-Ninjas API endpoint '/v1/airports' to fetch information about airports.

    Radius:
    - The function searches for airports within a 50-kilometer radius of the input coordinates.

    Error Handling:
    - If the API key is invalid or has expired, the function raises a ValueError.

    """
    key = "LeLHVfX2J+40J2TpuXen7A==JckrqmRp99HGwL2a"

    url = "https://api.api-ninjas.com"
    uri_nearest_airport = "/v1/airports"
    radius = 50 

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

    if len(airports) != 0:
        try:
            a = airports[0]["latitude"]
        except:
            raise ValueError("Api key is invalid or has expired. Please request a new one.")

    for airport in airports:
        distance = haversine(coords[0],coords[1], float(airport["latitude"]), float(airport["longitude"]))

        
        if distance <= radius:
            
            airport["distance"] = distance
            result.append(airport)

    return result

# Example
#get_airports("London", (51.5073509,-0.1277583)) # gets airports in London that are within 50 km of the input coordinates
