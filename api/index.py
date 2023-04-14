"""
Weather Bot it tells the weather forcast using OpenWeatherMap API
"""
import logging
import os
import sys
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
# from dotenv import dotenv_valueis
from os import getenv

from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel
sys.path.append('..')

openWeatherAPI = os.environ.get("OPEN_WEATHER_API_KEY")
base_url = "http://api.openweathermap.org/data/2.5/weather?"
import requests

# import weatherAPI
# import weatherAPI
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

# from ... import weatherAPI

TOKEN = os.environ.get("TELEGRAM_TOKEN_KEY")

app = FastAPI()

logging.basicConfig(format="%(asctime)s - %(name)s - %(message)s", level=logging.INFO)

class TelegramWebhook(BaseModel):
    update_id: int
    message: Optional[dict]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]
    shipping_query: Optional[dict]
    pre_checkout_querry: Optional[dict]
    poll: Optional[dict]
    poll_answer: Optional[dict]

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE)->None:
    await update.message.reply_text(text="""use 
    /weather to know general weather info
    /cord to get info about the coordinate
    /cloud to get info about the cloudes
    /wind to get info about the wind
    /other to get other info

    The default location is Addis Ababa
    to change city /city "City Name"
    """)

async def city(update: Update, context:ContextTypes.DEFAULT_TYPE)->None:
    chat_id = update.effective_message.chat_id
    cityN = str(context.args[0])
    await update.effective_message.reply_text(text=cityN)


async def coordWeather(update: Update, context:ContextTypes.DEFAULT_TYPE)->None:
    rtrn = WeatherAPI().coordInfo()
    await update.message.reply_text(text="Latitude: " + rtrn[0] + "\nLongtiude: " + rtrn[1])

async def genralWeather(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
    # returns genreal weather info(cur_temp, weather_desc, cur_humi)
    rtrn = WeatherAPI().mainInfo()
    await update.message.reply_text(text="Current temperature: "+rtrn[0]+
                                    "\nfeels like : "+rtrn[1]+
                                    "\nCurrent Pressure: "+rtrn[4]+
                                    "\nCurrent Humidity: "+rtrn[5]+
                                    "\nVisibility: "+rtrn[6]+
                                    "\nBase: "+rtrn[7])

async def cloudWeather(update: Update, context:ContextTypes.DEFAULT_TYPE)->None:
    rtrn = WeatherAPI().cloudWeatherInfo()
    await update.message.reply_text(text="Cloudeness: "+rtrn[0]+
                                    "\nGeneral weather info: "+rtrn[1]+
                                    "\nWeather description: "+rtrn[2])

async def windWeather(update: Update, context:ContextTypes.DEFAULT_TYPE)->None:
    rtrn = WeatherAPI().windInfo()
    await update.message.reply_text(text="Wind degre: "+rtrn[0]+
                                    "\nWind speed: "+rtrn[1])
async def otherWeather(update: Update, context:ContextTypes.DEFAULT_TYPE)->None:
    rtrn = WeatherAPI().otherInfo()
    await update.message.reply_text(text="CityName: "+str(rtrn[0])
                                    +"\nCountry code: "+rtrn[1]+
                                    "\nSun rise: "+rtrn[2]+
                                    "\nSun Set: "+rtrn[3])

def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler(["start", "help"], start))
    dispatcher.add_handler(CommandHandler("weather", genralWeather))
    dispatcher.add_handler(CommandHandler("cord", coordWeather))
    dispatcher.add_handler(CommandHandler("cloud", cloudWeather))
    dispatcher.add_handler(CommandHandler("wind", windWeather))
    dispatcher.add_handler(CommandHandler("other", otherWeather))
    dispatcher.add_handler(CommandHandler("city", city))
    

@app.post("/webhook")
def webhook(webhook_data: TelegramWebhook):
    bot = Bot(token=TOKEN)
    update = Update.de_json(webhook_data.dict(), bot)
    dispatcher = Application.builder().token(TOKEN).build()
    register_handlers(dispatcher)
    dispatcher.process_update(update)
    return {"message": "ok"}

@app.get("/")
def index():
    return {"message": "Good to go"}
# def main()->None:
#     application=Application.builder().token(TOKEN).read_timeout(40).write_timeout(40).build()
#     application.add_handler(CommandHandler(["start", "help"], start))
#     application.add_handler(CommandHandler("weather", genralWeather))
#     application.add_handler(CommandHandler("cord", coordWeather))
#     application.add_handler(CommandHandler("cloud", cloudWeather))
#     application.add_handler(CommandHandler("wind", windWeather))
#     application.add_handler(CommandHandler("other", otherWeather))
#     application.add_handler(CommandHandler("city", city))
#     # await application.bot.set_webhook(url=getenv("WEBHOOK_HOST"))
#     # await application.update_queue.put(Update.de_json(data=text, bot=application.bot))
#     application.run_polling()



# if __name__ == "__main__":
#     main()
