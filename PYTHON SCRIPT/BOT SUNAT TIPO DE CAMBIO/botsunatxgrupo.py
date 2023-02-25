import os
import telebot
import yfinance as yf
import requests



URL = 'https://api.apis.net.pe/v1/tipo-cambio-sunat' #configuramos la url
#solicitamos la información y guardamos la respuesta en data.
respuesta = requests.get(URL)
respuesta = respuesta.json() #convertimos la respuesta en dict
compra = respuesta['compra']
venta = respuesta['venta']
fecha = respuesta['fecha']
total  = ('  Tipo de compra,  ' +  str(compra) + '  Tipo de Venta  ' + str(venta) + '  Fecha  ' + str(fecha) )


#print('Compra, ' + str(compra) + '! How are you?')

API_KEY = 'IDETELEGRAM'
ID = "IDGRUPOTELEGRAM"
bot = telebot.TeleBot(API_KEY)


#id = "IdDelUsuariooCanalAqui"
#token = "TokenAqui"

url = "https://api.telegram.org/bot" + API_KEY + "/sendMessage"
params = {
'chat_id': ID,

'text' : str(total)
}

requests.post(url, params=params)