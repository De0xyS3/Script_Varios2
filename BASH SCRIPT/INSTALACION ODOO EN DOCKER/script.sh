#!/bin/bash
sudo apt-get install figlet &> /dev/null
echo "Comprobando si Docker está instalado..."
if ! [ -x "$(command -v docker)" ]; then
  echo 'Docker is not installed. Installing...'
  figlet -f slant "Installing Docker" | pv -qL 10
  curl -fsSL https://get.docker.com -o get-docker.sh -s
  sh get-docker.sh
  rm get-docker.sh
  echo "Docker ha sido instalado"
else
  echo "Docker ya está instalado."
fi

echo "Comprobando si Docker Compose está instalado..."
if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Docker Compose no está instalado. Instalando..'
  figlet -f slant "Installing Docker Compose" | pv -qL 10
  curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose -s
  chmod +x /usr/local/bin/docker-compose
  echo "Se ha instalado Docker Compose."
else
  echo "Docker Compose ya está instalado."
fi

echo "Verificando si nginx esta instalado..."
if ! [ -x "$(command -v nginx)" ]; then
  echo 'nginx is not installed. Installing...'
  figlet -f slant "Installing Nginx" | pv -qL 10
  apt-get install nginx -y
  echo "Se ha instalado Nginx."
else
  echo "Nginx ya esta instalado."
fi

echo "Seleccione la versión de Odoo que desea utilizar:"
echo "1) Versión oficial"
echo "2) Imagen personalizada"
read version_num

case $version_num in
    1)
        echo "Seleccione la versión comunity oficial de Odoo que desea utilizar: "
        echo "1) 14.0"
        echo "2) 15.0"
        echo "3) 16.0"
        read official_version_num

        case $official_version_num in
            1)
                odoo_version="odoo:14.0"
                postgres_version="13"
                ;;
            2)
                odoo_version="odoo:15.0"
                postgres_version="14.0"
                ;;
            3)
                odoo_version="odoo:16.0"
                postgres_version="latest"
                ;;
            *)
                echo "Opción inválida"
                exit 1
        esac
        ;;
    2)
        echo "Ingrese el nombre de la imagen personalizada de Odoo:"
        read odoo_version
        echo "Ingrese la versión de Postgres:"
        read postgres_version
        ;;
    *)
        echo "Opción inválida"
        exit 1
esac
# Pedir al usuario que ingrese la contraseña de la base de datos
read -p "Ingresa la contraseña de la base de datos: " db_password

echo "Ingresa el puerto a utilizar:"
read port_num
echo "Ingresa el nombre del contenedor a utilizar:"
read container_name

if [ ! -d "/root/docker/$container_name" ]; then
  #Create the directory
  mkdir -p /root/docker/$container_name
fi

cd /root/docker/$container_name && mkdir custom-addons

touch /root/docker/$container_name/docker-compose.yml
cat > /root/docker/$container_name/docker-compose.yml << EOL
version: '3.3'

services:

  odoo:
    image: $odoo_version
    container_name: $container_name
    restart: unless-stopped
    links:
      - db:db
    depends_on:
      - db
    ports:
      - "$port_num:8069"
    volumes:
      - odoo-data:/var/lib/odoo
      - ./odoo.conf:/etc/odoo/odoo.conf
      - ./custom-addons:/mnt/extra-addons

  db:
    image: postgres:$postgres_version
    container_name: db-$container_name
    restart: unless-stopped
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  odoo-data:
  db-data:
EOL

cat > /root/docker/$container_name/odoo.conf <<EOF
[options]
   ; This is the password that allows database operations:
addons_path = /mnt/extra-addons
admin_passwd = $db_password
csv_internal_sep = ,
data_dir = /var/lib/odoo/.local/share/Odoo
db_host = db
db_maxconn = 64
db_name = False
db_password = odoo
db_port = 5432
db_sslmode = prefer
db_template = template0
db_user = odoo
email_from = False
http_enable = True
http_interface =
http_port = 8069
import_partial =
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
limit_request = 2048
limit_time_cpe = 600
limit_time_cpu = 60
limit_time_real = 1200
limit_time_real_cron = -1
list_db = True
log_db = False
log_db_level = warning
log_handler = :INFO
log_level = info
logfile = /var/log/odoo/odoo.log
longpolling_port = 8072
max_cron_threads = 2
osv_memory_age_limit = False
osv_memory_count_limit = False
proxy_mode = True
reportgz = False
screencasts =
screenshots = /tmp/odoo_tests
server_wide_modules = base,web
syslog = False
test_enable = False
test_file =
test_tags = None
transient_age_limit = 1.0
translate_modules = ['all']
unaccent = False
upgrade_path =
without_demo = False
workers = 2
EOF
cd /root/docker/$container_name
docker-compose up -d
docker exec -u root $container_name apt update
docker exec -u root $container_name pip3 install paramiko
docker exec -u root $container_name sed -i '$a deb http://security.ubuntu.com/ubuntu bionic-security main' /etc/apt/sources.list
docker exec -u root $container_name apt update
docker exec -u root $container_name apt-cache policy libssl1.0-dev
docker exec -u root $container_name apt install -y libssl1.0-dev
docker exec -u root  $container_name apt install -y --only-upgrade odoo
sleep 2
docker-compose restart

echo "Deseas instalar certificado SSL let's encrypt  ? [y,n]"
read input


if [ "$input" == "" ]; then

   echo "Deseas instalar > SI o NO"

elif [[ "$input" == "y" ]] || [[ "$input" == "yes" ]]; then

sudo apt install python3-certbot-nginx
sudo certbot --nginx certonly
wget https://raw.githubusercontent.com/De0xyS3/odoo_ssl/main/nginx.sh
chmod +x nginx.sh
./nginx.sh
# treat anything else as a negative response
else
   echo "Anulado"

fi