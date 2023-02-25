import os
import telebot
import yfinance as yf
import requests

URL = 'https://api.apis.net.pe/v1/tipo-cambio-sunat'
respuesta = requests.get(URL)
respuesta = respuesta.json()
compra = respuesta['compra']
venta = respuesta['venta']
fecha = respuesta['fecha']
total = ( 'Tipo de Compra  '  + str(compra)   + 
'    Tipo de Venta   '+   str(venta)   +
 '   Fecha   '+   str(fecha)  )

API_KEY = 'IDDETELEGRAM'
bot = telebot.TeleBot (API_KEY)

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message,total)

bot.polling()