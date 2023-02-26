#!/bin/bash

# Pedir al usuario que ingrese la ruta del script
echo "Ingrese la ruta completa del script Battery_checker.py:"
read script_path

# Crear el archivo del servicio
sudo tee /etc/systemd/system/battery-checker.service > /dev/null <<EOF
[Unit]
Description=Comprueba el estado de la batería y apaga el servidor remoto si es necesario

[Service]
User=$USER
ExecStart=/usr/bin/python3 $script_path
ExecStartPre=/bin/sleep 1h
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Recargar los archivos de systemd
sudo systemctl daemon-reload

# Habilitar el servicio para que se ejecute al inicio
sudo systemctl enable battery-checker.service

# Iniciar el servicio
sudo systemctl start battery-checker.service

# Verificar el estado del servicio
sudo systemctl status battery-checker.service
