import requests
import urllib.parse
import datetime
import pytz, timezonefinder

weather_url = "https://api.openweathermap.org/data/2.5/weather?"
key = "20e8cba3d45624f174ec5764153e239c" #generate your api key

def get_weather(lat:float,lon:float, key:str)->tuple:
    """
    Get the information on the weather and current time

    Parameters:
        lat : latitude of the localization
        lon : longitude of the localization
        key : API Key used to do the request

    Returns:
        description : weather
        current_temp_C : current temperature in Celsius
        current_time : current time at destination
        icon_url : URL of the icon
    """
    url = weather_url + urllib.parse.urlencode({"lat":lat, "lon":lon, "appid":key})
    res = requests.get(url)
    print(res.status_code)
    if res.status_code == 200:
        data = res.json() #data en brut

    if data:
        icon = data["weather"][0]["icon"] #icon ID
        description = data["weather"][0]["description"] #current weather
        current_temp_K = data["main"]["temp"] #temperature in Kelvin
        current_temp_C = round(current_temp_K - 273.15) #temperature in Celcius
        icon_url = f'http://openweathermap.org/img/wn/{icon}.png' #icon link
        
        tf = timezonefinder.TimezoneFinder()
        # From the lat/long, get the tz-database-style time zone name or None
        timezone_str = tf.certain_timezone_at(lat=lat, lng=lon)
        if timezone_str is None:
            current_time = None
        else:
            timezone = pytz.timezone(timezone_str)
            dt = datetime.datetime.now(timezone)
            current_time = dt.strftime("%H:%M") #get the time in Hours/minutes
    return [description, current_temp_C, current_time, icon_url]

#print(get_weather(37.566535, 126.9779692, "20e8cba3d45624f174ec5764153e239c"))

