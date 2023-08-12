#!/bin/bash

# Solicitar información al usuario
read -p "Ingrese el nombre del acceso directo: " nombre_acceso_directo
read -p "Ingrese la ruta del icono (ruta completa): " ruta_icono
read -p "Ingrese la ruta de la aplicación a ejecutar (ruta completa): " ruta_aplicacion

# Crear el archivo .desktop en el directorio de accesos directos del usuario
echo "[Desktop Entry]
Name=$nombre_acceso_directo
Exec=$ruta_aplicacion
Icon=$ruta_icono
Terminal=false
Type=Application" > "$HOME/.local/share/applications/$nombre_acceso_directo.desktop"

echo "Acceso directo creado: $nombre_acceso_directo"
