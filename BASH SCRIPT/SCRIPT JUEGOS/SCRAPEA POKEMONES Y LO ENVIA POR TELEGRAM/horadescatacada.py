# Importación de las bibliotecas necesarias
import telegram
from selenium import webdriver
from bs4 import BeautifulSoup
import asyncio

# Creación del bot de Telegram
bot = telegram.Bot(token="ID")

# Inicialización del navegador y carga de la página web
driver = webdriver.Chrome()
driver.get("https://moonani.com/PokeList/spotlight_hour.php")

# Obtención del HTML de la página
html = driver.page_source

# Creación de un objeto BeautifulSoup con el HTML
soup = BeautifulSoup(html, "html.parser")

# Búsqueda de todas las tablas en el HTML
tables = soup.find_all("table")

# Iteración sobre las tablas
for table in tables:
    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        message = "`Hora Destacada en :   " + " | ".join([cell.text for cell in cells])
        
        # Si alguna celda de la fila contiene la palabra "texto", se envía el mensaje por Telegram
        if "m" in message: ##cambiar de preferencia
            # Función asíncrona para enviar el mensaje por Telegram
            async def main():
                await bot.send_message(chat_id="@pokebotfly", text=message)
            
            # Creación del bucle de eventos
            loop = asyncio.get_event_loop()

            # Ejecución del bucle de eventos hasta que se complete la tarea asíncrona
            loop.run_until_complete(main())

# Cierre del navegador
driver.close()
