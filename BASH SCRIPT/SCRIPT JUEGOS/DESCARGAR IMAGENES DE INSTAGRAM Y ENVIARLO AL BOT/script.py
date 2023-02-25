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
    driver.get("https://www.instagram.com/pokemongoappla/")

    # Espera a que se cargue la página y se muestre el primer post
    wait = WebDriverWait(driver, 1)
    wait.until(presence_of_element_located((By.CSS_SELECTOR, "article img")))

    # Búsqueda de todos los posts de la página
    posts = driver.find_elements(By.CSS_SELECTOR, "article img")

    # Iteración sobre los posts
    for post in posts:
        # Envío del post por Telegram
        await bot.send_photo(chat_id="@pokebotfly", photo=post.get_attribute("src"))

    # Cierre del navegador
    driver.close()

# Ejecución del bucle de eventos hasta que se complete la tarea asíncrona
asyncio.run(main())
