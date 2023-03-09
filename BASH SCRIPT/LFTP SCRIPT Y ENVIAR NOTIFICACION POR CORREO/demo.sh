#!/bin/bash

# Configuración de variables
SFTP_HOST='nombre_del_servidor_remoto'
SFTP_USERNAME='nombre_de_usuario'
SFTP_PASSWORD='contraseña_del_usuario'
SFTP_REMOTE_FILE='/ruta/al/archivo_remoto'
EMAIL_RECIPIENT='correo_destinatario@example.com'
EMAIL_SUBJECT='Asunto del correo'
EMAIL_BODY='Cuerpo del correo'

# Descarga del archivo remoto
sftppass -P $SFTP_PASSWORD sftp $SFTP_USERNAME@$SFTP_HOST << EOF
  get $SFTP_REMOTE_FILE
  quit
EOF

# Lectura del contenido del archivo
FILE_CONTENTS=$(cat $(basename $SFTP_REMOTE_FILE))

# Envío del correo electrónico con el contenido del archivo
echo "$EMAIL_BODY"$'\n\n'"$FILE_CONTENTS" | mail -s "$EMAIL_SUBJECT" $EMAIL_RECIPIENT

# Eliminación del archivo descargado
rm $(basename $SFTP_REMOTE_FILE)
