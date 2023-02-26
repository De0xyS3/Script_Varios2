import paramiko
import requests
import time
from bs4 import BeautifulSoup
import telegram
import asyncio

# Función para apagar el servidor remoto
def shutdown_server():
    # Conexión al servidor remoto
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    while True:
        try:
            ssh.connect('192.168.1.23', username='root', password='r0m4n0s.1507')
            break
        except:
            print("No se puede conectar por SSH. Esperando 60 segundos...")
            time.sleep(60)

    # Ejecución del comando para apagar el servidor
    ssh.exec_command('shutdown -h now')

    # Cierre de la conexión SSH
    ssh.close()



# Función para enviar un mensaje por Telegram
def send_telegram_message(bot_token, chat_id, message):
    bot = telegram.Bot(token=bot_token)
    bot.send_message(chat_id=chat_id, text=message)

# Función principal del script
def main():
    # URL de la página web a verificar
    url = 'http://192.168.1.9:5000/'


    while True:
        # Realizar una solicitud GET a la página web
        response = requests.get(url)

        # Analizar el HTML para obtener el estado de la batería
        soup = BeautifulSoup(response.text, 'html.parser')
        battery_state = soup.find(id='battery-state').get_text().strip()

        # Imprimir el estado de la batería
        print(f'Estado de la batería: {battery_state}')

        # Verificar el estado de la batería
        if response.status_code == 200 and battery_state == '100':
            print('Batería al 50%. Apagando el servidor remoto...')
            shutdown_server()
            #break

        # Esperar 20 segundos antes de realizar la siguiente comprobación
        time.sleep(20)
#Envio de notificacion
async def send_telegram_message():
    bot = telegram.Bot(token='INGRESA_TOKEN_BOT')
    await bot.send_message('INGRESA_ID', text='Las baterias del UPS han llegado al 50% se realizara el apagado del servidor TRUENAS...')
asyncio.run(send_telegram_message())

# Ejecución de la función principal
if __name__ == '__main__':
    main()
