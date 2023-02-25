##sudo apt-get install mailutils para debian/ubuntu

##sudo yum install mailx para centos

# FTP LOGIN
HOST='sftp://ftp.domain.com'
USER='ftpusername'
PASSWORD='ftppassword'

# DISTANT DIRECTORY
REMOTE_DIR='/absolute/path/to/remote/directory'

#LOCAL DIRECTORY
LOCAL_DIR='/absolute/path/to/local/directory'

# RUNTIME!
echo
echo "Starting download $REMOTE_DIR from $HOST to $LOCAL_DIR"
date

lftp -u "$USER","$PASSWORD" $HOST <<EOF
# the next 3 lines put you in ftpes mode. Uncomment if you are having trouble connecting.
# set ftp:ssl-force true
# set ftp:ssl-protect-data true
# set ssl:verify-certificate no
# transfer starts now...
set sftp:auto-confirm yes
mirror --use-pget-n=10 $REMOTE_DIR $LOCAL_DIR;
exit
EOF
echo
echo "Transfer finished"
date

# Configuración del servidor SMTP
SMTP_SERVER="smtp.example.com"
SMTP_PORT="587"
SMTP_USERNAME="tu_usuario"
SMTP_PASSWORD="tu_contraseña"
FROM_EMAIL="correo_emisor@example.com"
TO_EMAIL="correo_destinatario@example.com"
SUBJECT="Transferencia de archivo completada"
BODY="La transferencia del archivo $REMOTE_DIR desde $HOST a $LOCAL_DIR se ha completado."

# Envío de correo electrónico utilizando mailx
echo "$BODY" | mailx \
    -s "$SUBJECT" \
    -S smtp="$SMTP_SERVER":"$SMTP_PORT" \
    -S smtp-use-starttls \
    -S smtp-auth=login \
    -S smtp-auth-user="$SMTP_USERNAME" \
    -S smtp-auth-password="$SMTP_PASSWORD" \
    -r "$FROM_EMAIL" \
    "$TO_EMAIL"
