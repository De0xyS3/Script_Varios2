from bs4 import BeautifulSoup
import requests

url = 'http://192.168.1.9:5000/'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    battery_state = soup.find(id='battery-state').get_text().strip()
    if battery_state == '100':
        exec(open('battery_consulting.py').read())


###SI DEESEAS CARGAR VARIOS SCRIPTS DESCOMENTA ESTAS LINEAS

# import subprocess
# import time
# import os
# from bs4 import BeautifulSoup
# import requests

# # Función para ejecutar un script Python
# def run_python_script(script_path):
#     subprocess.Popen(['python3', script_path])

# # URL de la página web a verificar
# url = 'http://192.168.1.9:5000/'

# while True:
#     # Realizar una solicitud GET a la página web
#     response = requests.get(url)

#     # Analizar el HTML para obtener el estado de la batería
#     soup = BeautifulSoup(response.text, 'html.parser')
#     battery_state = soup.find(id='battery-state').get_text().strip()

#     # Imprimir el estado de la batería
#     print(f'Estado de la batería: {battery_state}')

#     # Verificar el estado de la batería
#     if response.status_code == 200 and battery_state == '100':
#         print('Batería al 100%. Ejecutando script...')
#         # Ruta del directorio que contiene los scripts a ejecutar
#         script_directory = '/home/user/scripts/'
#         # Iterar sobre los archivos en el directorio de scripts
#         for file_name in os.listdir(script_directory):
#             # Verificar si el archivo es un script Python
#             if file_name.endswith('.py'):
#                 # Obtener la ruta completa del script
#                 script_path = os.path.join(script_directory, file_name)
#                 # Ejecutar el script
#                 run_python_script(script_path)
#         break
