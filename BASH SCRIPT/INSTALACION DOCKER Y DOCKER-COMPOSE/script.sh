#!/bin/sh

sudo apt-get install figlet pv &> /dev/null
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
fi &> /dev/null
