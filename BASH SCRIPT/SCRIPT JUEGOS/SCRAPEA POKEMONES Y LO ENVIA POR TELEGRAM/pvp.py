# Importación de las bibliotecas necesarias
import telegram
from selenium import webdriver
from bs4 import BeautifulSoup
import asyncio

# Creación del bot de Telegram
bot = telegram.Bot(token="ID")

# Inicialización del navegador y carga de la página web
driver = webdriver.Chrome()
driver.get("https://moonani.com/PokeList/pvp.php")

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
        message = " | ".join([cell.text for cell in cells])

    


async def main():
    # Envío del mensaje por Telegram
    await bot.send_message(chat_id="@pokebotfly", text=message)

# Ejecución del bucle de eventos
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()


# Cierre del navegador
driver.close()



### for lINUX ###

# Importación de las bibliotecas necesarias

import telegram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import asyncio

options = Options()
# Creación del bot de Telegram

bot = telegram.Bot(token="5947634113:AAHMuHTblIZdVxR6T7y0b18Oen5Q9ey_yQ8")
# Inicialización del navegador y carga de la página web
driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
options.binary_location = "/usr/bin/google-chrome"
options.add_argument('headless')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
#driver = webdriver.chrome(options=options)
driver.get("https://moonani.com/PokeList/pvp.php")
# Obtención del HTML de la página
html = driver.page_source
# Creación de un objeto BeautifulSoup con el HTMLs
soup = BeautifulSoup(html, "html.parser")
# Búsqueda de todas las tablas en el HTML
tables = soup.find_all("table")



# Iteración sobre las tablas

for table in tables:

    rows = table.find_all("tr")

    for row in rows:

        cells = row.find_all("td")

        message ="Nuevo Pokemon PVP encontrado  "+ " | ".join([cell.text for cell in cells])



    





async def main():

    # Envío del mensaje por Telegram

    await bot.send_message(chat_id="@pokebotfly", text=message)



# Ejecución del bucle de eventos

loop = asyncio.get_event_loop()

loop.run_until_complete(main())

loop.close()





# Cierre del navegador

driver.close()


####CRONTAB * * * * * export DISPLAY=:0 && export PATH=$PATH:/usr/local/bin && /usr/bin/python3 /home/username/Documents/Project/project.py####