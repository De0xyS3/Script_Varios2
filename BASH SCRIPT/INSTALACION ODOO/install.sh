#!/bin/bash

# Pedir al usuario que ingrese el dominio que desea utilizar para su instalación de Odoo
read -p "Ingresa el dominio que deseas utilizar para tu instalación de Odoo: " domain

# Pedir al usuario que seleccione la versión de Odoo que desea instalar
echo "Selecciona la versión de Odoo que deseas instalar:"
echo "1) Odoo 16"
echo "2) Odoo 15"
echo "3) Odoo 14"
echo "4) Odoo 13"
echo "5) Odoo 12"
echo "6) Odoo 11"

read -p "Selección: " odoo_version

# Asignar la versión de Odoo seleccionada a una variable
if [ $odoo_version == 1 ]; then
    odoo_version=16
elif [ $odoo_version == 2 ]; then
    odoo_version=15
elif [ $odoo_version == 3 ]; then
    odoo_version=14
elif [ $odoo_version == 4 ]; then
    odoo_version=13
elif [ $odoo_version == 5 ]; then
    odoo_version=12
 elif [ $odoo_version == 6 ]; then
    odoo_version=11
     
fi

# Pedir al usuario que ingrese la contraseña de la base de datos
read -p "Ingresa la contraseña de la base de datos: " db_password

# Pedir al usuario si desea instalar el paquete wkhtmltopdf
read -p "¿Deseas instalar el paquete wkhtmltopdf? (s/n) " install_wkhtmltopdf

# Pedir al usuario si desea instalar el servicio nginx
read -p "¿Deseas instalar el servicio nginx? (s/n) " install_nginx

# Actualizar la lista de paquetes disponibles y actualizar los paquetes instalados
sudo apt-get update && sudo apt-get upgrade -y

# Instalar los paquetes necesarios para la instalación de Odoo
sudo apt install git python3-pip build-essential wget python3-dev python3-venv \
    python3-wheel libfreetype6-dev libxml2-dev libzip-dev libldap2-dev libsasl2-dev \
    python3-setuptools node-less libjpeg-dev zlib1g-dev libpq-dev \
    libxslt1-dev libldap2-dev libtiff5-dev libjpeg8-dev libopenjp2-7-dev \
    liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev
    
# Instalar los paquetes Node.js y NPM
apt-get install npm 
npm install -g less less-plugin-clean-css
apt-get install node-less

# Instalar el paquete wkhtmltopdf si el usuario lo ha seleccionado
if [ $install_wkhtmltopdf == "s" ]; then
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb
dpkg -i wkhtmltox_0.12.6-1.bionic_amd64.deb
apt-get install -f
fi

# Instalar el servicio nginx si el usuario lo ha seleccionado
if [ $install_nginx == "s" ]; then
    sudo apt-get install nginx -y
fi

# Instalacion de  PostgreSQl
apt-get install postgresql -y
sudo su - postgres -c "createuser -s odoo$odoo_version"


# Agregando Usuario Odoo
useradd -m -d /opt/odoo$odoo_version -U -r -s /bin/bash odoo$odoo_version

# Descargar el código fuente de Odoo desde GitHub
cd /opt/odoo$odoo_version && git clone --depth 1 --branch $odoo_version.0 https://www.github.com/odoo/odoo --single-branch

pip3 install -r /opt/odoo$odoo_version/odoo/requirements.txt
# Crear un archivo de configuración para la instalación de Odoo

cat > /etc/odoo.conf <<EOF
[options]
   ; This is the password that allows database operations:
   admin_passwd = $db_password
   db_host = False
   db_port = False
   db_user = odoo$odoo_version
   db_password = False
   xmlrpc_interface = 127.0.0.1
   proxy_mode = True
   addons_path = /opt/odoo$odoo_version/odoo/addons
   logfile = /var/log/odoo/odoo.log
EOF

chown odoo$odoo_version: /etc/odoo.conf
rm  -r /var/log/odoo
mkdir /var/log/odoo
chown odoo$odoo_version:root /var/log/odoo

cat >  /etc/systemd/system/odoo$odoo_version.service<<EOF

[Unit]
   Description=Odoo
   Documentation=http://www.odoo.com
[Service]
   Type=simple
   User=odoo$odoo_version
   ExecStart=/opt/odoo$odoo_version/odoo/odoo-bin -c /etc/odoo.conf
[Install]
   WantedBy=default.target
EOF

systemctl daemon-reload
systemctl start odoo$odoo_version
systemctl enable odoo$odoo_version

touch /etc/nginx/conf.d/odoo$odoo_version.conf
cat > /etc/nginx/conf.d/odoo$odoo_version.conf<<EOF
upstream odoo {
 server 127.0.0.1:8069;
}
upstream odoochat {
 server 127.0.0.1:8072;
}
server {
 listen 80;
 server_name $domain;
 proxy_read_timeout 720s;
 proxy_connect_timeout 720s;
 proxy_send_timeout 720s;
 # Add Headers for odoo proxy mode
 proxy_set_header X-Forwarded-Host \$host;
 proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
 proxy_set_header X-Forwarded-Proto \$scheme';
 proxy_set_header X-Real-IP \$remote_addr';
 # log
 access_log /var/log/nginx/odoo.access.log;
 error_log /var/log/nginx/odoo.error.log;
 # Redirect longpoll requests to odoo longpolling port
 location /longpolling {
 proxy_pass http://odoochat;
 }
 # Redirect requests to odoo backend server
 location / {
   proxy_redirect off;
   proxy_pass http://odoo;
 }
 # common gzip
 gzip_types text/css text/scss text/plain text/xml application/xml application/json application/javascript;
 gzip on;
}
EOF

# Reiniciando serivicios NGINX
systemctl restart nginx

# Configurar el servicio de Odoo para iniciarse automáticamente al iniciar el sistema
sudo systemctl enable odoo$odoo_version
sudo service odoo$odoo_version start
