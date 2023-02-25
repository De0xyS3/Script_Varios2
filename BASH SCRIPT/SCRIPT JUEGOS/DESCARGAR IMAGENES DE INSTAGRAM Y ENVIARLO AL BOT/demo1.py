# Importación de las bibliotecas necesarias
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import telegram

# Creación del bot de Telegram
bot = telegram.Bot(token="TOKENID")

async def main():
    # Inicialización del navegador y carga de la página de Instagram
    driver = webdriver.Chrome(executable_path="/path/to/chromedriver")
    driver.get("https://www.instagram.com/legendslima/")

    # Espera a que se cargue la página y se muestre el primer post
    wait = WebDriverWait(driver, 5)
    wait.until(presence_of_element_located((By.CSS_SELECTOR, "article img")))

    # Búsqueda del último post de la página
    post = driver.find_elements(By.CSS_SELECTOR, "article img")[-12]
# Obtención de la descripción del post
   # description = driver.find_element(By.CSS_SELECTOR, "article div div div div p").text
    # Envío del último post por Telegram
    await bot.send_photo(chat_id="@pokebotfly", photo=post.get_attribute("src"))
    #await bot.send_message(chat_id="@pokebotfly", text=description)
    # Cierre del navegador
    driver.close()

# Ejecución del bucle de eventos hasta que se complete la tarea asíncrona
asyncio.run(main())
