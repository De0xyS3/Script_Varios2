import telegram
import requests
import time

from bs4 import BeautifulSoup

# Creación del bot de Telegram
bot = telegram.Bot(token="ID")

# Dirección URL de la página web que quieres monitorizar
URL = "https://www3.animeflv.net/"

# Función que comprueba si hay nuevo contenido en la página web
def check_new_content():
    # Descarga del HTML de la página web
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    # Búsqueda de un elemento específico en el HTML (por ejemplo, un título o una sección)
    elements = soup.find_all("div", {"class": "ListEpisodios AX Rows A06 C04 D03"})

    # Si se encuentra el elemento, se envía un mensaje por Telegram
    if elements:
        bot.send_message(chat_id="IDEDELACUENTA", text="Se ha añadido nuevo contenido a la página web")

# Ejecución de la función cada 10 minutos
while True:
    check_new_content()
    time.sleep(600)
