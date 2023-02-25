import paramiko
import requests
import time

# Función para apagar el servidor remoto
def shutdown_server():
    # Conexión al servidor remoto
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.1.7', username='username', password='password')
    
    # Ejecución del comando para apagar el servidor
    ssh.exec_command('sudo init 0')

    # Cierre de la conexión SSH
    ssh.close()

# Función principal del script
def main():
    # URL de la página web a verificar
    url = 'http://192.168.1.9:5000/'

    while True:
        # Realizar una solicitud GET a la página web
        response = requests.get(url)

        # Verificar el estado de la batería
        if response.status_code == 200 and response.text.strip() == '50':
            print('Batería al 50%. Apagando el servidor remoto...')
            shutdown_server()
            break

        # Esperar 20 segundos antes de realizar la siguiente comprobación
        time.sleep(20)

# Ejecución de la función principal
if __name__ == '__main__':
    main()



