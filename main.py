"""
Weather Bot it tells the weather forcast using OpenWeatherMap API
"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
# from dotenv import dotenv_valueis

from weatherAPI import *

TOKEN = os.environ.get("TELEGRAM_TOKEN_KEY")

logging.basicConfig(format="%(asctime)s - %(name)s - %(message)s", level=logging.INFO)

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE)->None:
    await update.message.reply_text("""use 
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
    await update.effective_message.reply_text(cityN)


async def coordWeather(update: Update, context:ContextTypes.DEFAULT_TYPE)->None:
    rtrn = WeatherAPI().coordInfo()
    await update.message.reply_text("Latitude: " + rtrn[0] + "\nLongtiude: " + rtrn[1])

async def genralWeather(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
    # returns genreal weather info(cur_temp, weather_desc, cur_humi)
    rtrn = WeatherAPI().mainInfo()
    await update.message.reply_text("Current temperature: "+rtrn[0]+
                                    "\nfeels like : "+rtrn[1]+
                                    "\nCurrent Pressure: "+rtrn[4]+
                                    "\nCurrent Humidity: "+rtrn[5]+
                                    "\nVisibility: "+rtrn[6]+
                                    "\nBase: "+rtrn[7])

async def cloudWeather(update: Update, context:ContextTypes.DEFAULT_TYPE)->None:
    rtrn = WeatherAPI().cloudWeatherInfo()
    await update.message.reply_text("Cloudeness: "+rtrn[0]+
                                    "\nGeneral weather info: "+rtrn[1]+
                                    "\nWeather description: "+rtrn[2])

async def windWeather(update: Update, context:ContextTypes.DEFAULT_TYPE)->None:
    rtrn = WeatherAPI().windInfo()
    await update.message.reply_text("Wind degre: "+rtrn[0]+
                                    "\nWind speed: "+rtrn[1])
async def otherWeather(update: Update, context:ContextTypes.DEFAULT_TYPE)->None:
    rtrn = WeatherAPI().otherInfo()
    await update.message.reply_text("CityName: "+str(rtrn[0])
                                    +"\nCountry code: "+rtrn[1]+
                                    "\nSun rise: "+rtrn[2]+
                                    "\nSun Set: "+rtrn[3])

def main()->None:
    application=Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("weather", genralWeather))
    application.add_handler(CommandHandler("cord", coordWeather))
    application.add_handler(CommandHandler("cloud", cloudWeather))
    application.add_handler(CommandHandler("wind", windWeather))
    application.add_handler(CommandHandler("other", otherWeather))
    application.run_polling()

if __name__ == "__main__":
    main()
