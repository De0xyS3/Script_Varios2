import paramiko
import smtplib
from email.mime.text import MIMEText

# Configuración de variables
SFTP_HOST = 'nombre_del_servidor_remoto'
SFTP_USERNAME = 'nombre_de_usuario'
SFTP_PASSWORD = 'contraseña_del_usuario'
SFTP_REMOTE_FILE = '/ruta/al/archivo_remoto'
EMAIL_RECIPIENT = 'correo_destinatario@example.com'
EMAIL_SUBJECT = 'Asunto del correo'
EMAIL_BODY = 'Cuerpo del correo'

# Conexión al servidor SFTP
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(SFTP_HOST, username=SFTP_USERNAME, password=SFTP_PASSWORD)
sftp = ssh.open_sftp()

# Lectura del contenido del archivo remoto
remote_file = sftp.open(SFTP_REMOTE_FILE, 'r')
file_contents = remote_file.read()
remote_file.close()

# Envío del correo electrónico con el contenido del archivo
msg = MIMEText(EMAIL_BODY + '\n\n' + file_contents)
msg['Subject'] = EMAIL_SUBJECT
msg['From'] = EMAIL_RECIPIENT
msg['To'] = EMAIL_RECIPIENT
s = smtplib.SMTP('localhost')
s.sendmail(EMAIL_RECIPIENT, [EMAIL_RECIPIENT], msg.as_string())
s.quit()

# Cierre de la conexión SFTP
sftp.close()
ssh.close()
