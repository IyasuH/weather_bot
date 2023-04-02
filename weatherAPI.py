"""
handles weather request
"""
import requests
import os

openWeatherAPI = os.environ.get("OPEN_WEATHER_API_KEY")
base_url = "http://api.openweathermap.org/data/2.5/weather?"


class WeatherAPI():
              
    def __init__(self, cityName="Addis Ababa", unit="metric"):
        self.cityName = cityName
        self.unit = unit
        complete_url = base_url + "appid=" +openWeatherAPI+ "&q=" + self.cityName+"&units="+self.unit
        response = requests.get(complete_url)
        self.x = response.json()


    def coordInfo(self):
        if self.x["cod"] != "404":
            y=self.x["main"]
            coordI = self.x["coord"]
            coordLon = str(coordI["lon"])
            coordLat = str(coordI["lat"])
            return(coordLat, coordLon)
        else:
            print("Erorr 404")
            return (None)

    def mainInfo(self):
        if self.x["cod"] != "404":
            mainI=self.x["main"]
            cur_temp = str(round(mainI["temp"], 2)) + " °C"
            feels_like = str(mainI["feels_like"]) + " °C"
            max_temp = str(round(mainI["temp_max"], 2)) + " °C"
            min_temp = str(round(mainI["temp_min"], 2)) + " °C"
            # sea_lvl = str(mainI["sea_level"])
            # grn_lvl = str(mainI["grnd_level"])
            cur_pres = str(mainI["pressure"]) + " pascal"
            cur_humi = str(mainI["humidity"]) + " hygrometers"
            visibility = str(self.x["visibility"]) + " meter"# in m
            base = str(self.x["base"])
            return(cur_temp, feels_like, max_temp, min_temp, cur_pres, cur_humi, visibility, base)
        else:
            print("Erorr 404")
            return (None)

    def cloudWeatherInfo(self):
        if self.x["cod"] != "404":
            cloudsI =self.x["clouds"]
            clouds = str(cloudsI["all"]) + " %" # cloudiness %
            weatherI = self.x["weather"]
            weather_main = weatherI[0]["main"]
            weather_desc = weatherI[0]["description"]
            return(clouds, weather_main, weather_desc)
        else:
            print("Erorr 404")
            return (None)

    def windInfo(self):
        if self.x["cod"] != "404":
            windI = self.x["wind"]
            wind_deg = str(windI["deg"]) + " °"
            wind_speed = str(windI["speed"]) + " meter per second"
            # wind_gust = str(windI["gust"])
            return(wind_deg, wind_speed)
        else:
            print("Erorr 404")
            return (None)

    def otherInfo(self):
        if self.x["cod"] != "404":
            cityName = str(self.x["name"])
            sys = self.x["sys"]
            countryCode = str(sys["country"])
            sunrise = str(sys["sunrise"])
            sunset = str(sys["sunset"])
            return(cityName, countryCode, sunrise, sunset)
        else:
            print("Erorr 404")
            return (None)


