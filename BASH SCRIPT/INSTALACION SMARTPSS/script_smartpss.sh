#!/bin/bash
# URL de la lista blanca de IPs
whitelist_url="https://raw.githubusercontent.com/user/repo/master/whitelist.txt"

# Obtener la IP del usuario
user_ip=$(curl -s "https://api.ipify.org")

# Descargar la lista blanca de IPs y buscar la IP del usuario
if curl -s "$whitelist_url" | grep -q "$user_ip"; then

echo -e "\033[1;34mInstalando dependencias...\033[0m"
# Instala las dependencias utilizando apt y muestra el progreso con pv
apt install -y libfreetype6 libfontconfig1  2>&1 | pv -l > /dev/null
# Comprueba si la instalación ha sido exitosa
if [ $? -eq 0 ]
then
  # Muestra un mensaje de éxito en verde
  echo -e "\033[1;32mInstalación exitosa!\033[0m"
else
  # Muestra un mensaje de error en rojo
  echo -e "\033[1;31mError en la instalación.\033[0m"
fi

apt install pv -y
echo "Actualizando sistema..."
sudo apt update -y | pv -l > /dev/null
echo "Descargando y instalando dependencias..."
apt install wine -y | pv -l > /dev/null

sudo apt-get install -y zip
sudo apt-get install -y wine-stable
sudo apt install libfreetype6 libfontconfig1
wget https://dahuawiki.com/images/Files/Software/SmartPSS/DH_SMARTPSS-Win64_En_IS_V2.003.0000004.0.R.201021.zip
unzip DH_SMARTPSS-Win64_En_IS_V2.003.0000004.0.R.201021.zip
wine SmartPSS.exe

else
  # La IP del usuario no está en la lista blanca, mostrar un mensaje de error
  echo "Tu IP no está en la lista blanca de IPs permitidas para descargar el archivo"
fi


