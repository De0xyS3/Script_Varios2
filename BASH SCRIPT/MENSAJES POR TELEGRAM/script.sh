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

# Enviar notificación por Telegram
# Configuración del bot de Telegram
BOT_TOKEN="tu_token_de_bot"
CHAT_ID="tu_chat_id"

# Mensaje a enviar
MESSAGE="La transferencia del archivo $REMOTE_DIR desde $HOST a $LOCAL_DIR se ha completado."

# Envío de mensaje utilizando curl
curl -s -X POST \
    https://api.telegram.org/bot${BOT_TOKEN}/sendMessage \
    -d chat_id=${CHAT_ID} \
    -d text="${MESSAGE}"
