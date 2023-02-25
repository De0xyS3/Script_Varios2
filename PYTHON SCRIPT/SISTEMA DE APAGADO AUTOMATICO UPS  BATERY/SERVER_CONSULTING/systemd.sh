#!/bin/bash

# Pedir al usuario que ingrese la ruta del script
echo "Ingrese la ruta completa del connect_ups_monitor.py:"
read script_path

# Crear el archivo del servicio
sudo tee /etc/systemd/system/ups.service > /dev/null <<EOF
[Unit]
Description=Comprueba el estado de la batería a tiempo real
[Service]
User=$USER
ExecStart=/usr/bin/python3 $script_path
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Recargar los archivos de systemd
sudo systemctl daemon-reload

# Habilitar el servicio para que se ejecute al inicio
sudo systemctl enable ups.service

# Iniciar el servicio
sudo systemctl start ups.service

# Verificar el estado del servicio
sudo systemctl status ups.service
