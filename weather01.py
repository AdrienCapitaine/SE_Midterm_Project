import requests
import urllib.parse
from datetime import datetime 

weather_url = "https://api.openweathermap.org/data/2.5/weather?"
key = "dac4f1e3814dae0d9ad08b0ba1ed679e" #generate your api key

def get_weather(lat,lon, key):
    #url = "https://api.openweathermap.org/data/2.5/weather?lat=37.566535&lon=126.9779692&appid=20e8cba3d45624f174ec5764153e239c"
    url = weather_url + urllib.parse.urlencode({"lat":lat, "lon":lon, "appid":key})
    #print(url)
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json() #data en brut
        
    '''else:
        print("Erreur lors de la requête :", res.status_code)
        return None'''



    # data = get_weather(37.566535, 126.9779692, "20e8cba3d45624f174ec5764153e239c")
    if data:
        icon = data["weather"][0]["icon"] #id de l'icone
        main = data["weather"][0]["main"] #temps
        description = data["weather"][0]["description"] #temps détaillé
        current_temp_K = data["main"]["temp"] #température actuelle en kelvin
        current_temp_C = round(current_temp_K - 273.15)
        dt = data["dt"]
        icon_url = f'http://openweathermap.org/img/wn/{icon}.png' #lien png de l'icone
        time_at_dest = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')
    return [description, current_temp_C, time_at_dest, icon_url]

#print(get_weather(37.566535, 126.9779692, "20e8cba3d45624f174ec5764153e239c"))

