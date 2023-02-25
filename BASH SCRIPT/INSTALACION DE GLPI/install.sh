#!/bin/bash

# Instalar dependencias
apt update
apt install -y apache2 mariadb-server php7.2 libapache2-mod-php7.2
apt install -y php7.2-mysql php7.2-gd php7.2-curl php7.2-cli php7.2-common

# Descargar GLPI desde GitHub

echo "Seleccione la versión de GLPI que desea instalar:"
echo "1. GLPI 9.5.1"
echo "2. GLPI 9.6.0"
echo "3. GLPI 9.6.1"
echo "4. GLPI 9.6.2"
echo "5. GLPI 9.6.3"

read -p "Opción: " version

case $version in
    1)
        wget https://github.com/glpi-project/glpi/releases/download/9.5.1/glpi-9.5.1.tgz
        tar -xzvf glpi-9.5.1.tgz
        mv glpi /var/www/html/glpi
        chown -R www-data:www-data /var/www/html/glpi
        ;;
    2)
        wget https://github.com/glpi-project/glpi/releases/download/9.6.0/glpi-9.6.0.tgz
        tar -xzvf glpi-9.6.0.tgz
        mv glpi /var/www/html/glpi
        chown -R www-data:www-data /var/www/html/glpi
        ;;
    3)
        wget https://github.com/glpi-project/glpi/releases/download/9.6.1/glpi-9.6.1.tgz
        tar -xzvf glpi-9.6.1.tgz
        mv glpi /var/www/html/glpi
        chown -R www-data:www-data /var/www/html/glpi
        ;;
    4)
        wget https://github.com/glpi-project/glpi/releases/download/9.6.2/glpi-9.6.2.tgz
        tar -xzvf glpi-9.6.2.tgz
        mv glpi /var/www/html/glpi
        chown -R www-data:www-data /var/www/html/glpi
        ;;
    5)
        wget https://github.com/glpi-project/glpi/releases/download/9.6.3/glpi-9.6.3.tgz
        tar -xzvf glpi-9.6.3.tgz
        mv glpi /var/www/html/glpi
        chown -R www-data:www-data /var/www/html/glpi

# Configurar base de datos
mysql -u root -e "CREATE DATABASE glpi;"
mysql -u root -e "GRANT ALL PRIVILEGES ON glpi.* TO 'glpi'@'localhost' IDENTIFIED BY 'glpi';"

# Permisos de archivos
chown -R www-data:www-data /var/www/html/glpi
chmod -R 775 /var/www/html/glpi/files

# Reiniciar Apache
service apache2 restart

# Acceder a la instalación de GLPI desde un navegador web
echo "Accede a la siguiente URL para iniciar la instalación de GLPI: http://localhost/glpi/install/install.php"
