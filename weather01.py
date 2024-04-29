import requests
import urllib.parse
import datetime
import pytz, timezonefinder

weather_url = "https://api.openweathermap.org/data/2.5/weather?"

key = "20e8cba3d45624f174ec5764153e239c" #generate your api key

def get_weather(lat,lon, key):
    #url = "https://api.openweathermap.org/data/2.5/weather?lat=37.566535&lon=126.9779692&appid=20e8cba3d45624f174ec5764153e239c"
    url = weather_url + urllib.parse.urlencode({"lat":lat, "lon":lon, "appid":key})
    res = requests.get(url)

    #print(res.status_code)
    if res.status_code == 200:
        data = res.json() #data en brut

    if data:
        icon = data["weather"][0]["icon"] #id de l'icone
        main = data["weather"][0]["main"] #temps
        description = data["weather"][0]["description"] #temps détaillé
        current_temp_K = data["main"]["temp"] #température actuelle en kelvin
        current_temp_C = round(current_temp_K - 273.15)
        icon_url = f'http://openweathermap.org/img/wn/{icon}.png' #lien png de l'icone
        tf = timezonefinder.TimezoneFinder()

        # From the lat/long, get the tz-database-style time zone name (e.g. 'America/Vancouver') or None
        timezone_str = tf.certain_timezone_at(lat=lat, lng=lon)
        if timezone_str is None:
            # print("Could not determine the time zone")
            timezone = None
            dt = None
            current_time = None
        else:
            # Display the current time in that time zone
            timezone = pytz.timezone(timezone_str)
            dt = datetime.datetime.now(timezone)
            current_time = dt.strftime("%H:%M")
    return [description, current_temp_C, current_time, icon_url]

#print(get_weather(37.566535, 126.9779692, "20e8cba3d45624f174ec5764153e239c"))

