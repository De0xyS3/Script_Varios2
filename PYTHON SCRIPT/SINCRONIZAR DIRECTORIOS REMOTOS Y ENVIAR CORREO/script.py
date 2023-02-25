 
# PARA QUE EL SCRIPT FUNCIONE Y PUEDAS SINCRONIZAR DOS CARPETAS REMOTAS, PRIMERO DEBES MONTAR UNA CARPETA REMOTA A UNA CARPETA LOCA DEL EQUIPO
# DEBES TENER INSTALADO EN EL EQUIPO sshfs y sshpass
#sshfs soporte@192.168.1.21:/Backup03/ /mnt/serverB/
# 
#  Para desmontar la unidad montada con sshfs, puedes utilizar el siguiente comando:
# fusermount -u /mnt/serverB

#Este comando desmontará la unidad ubicada en /mnt/serverB. Si todavía tienes procesos ejecutándose en esa unidad, puedes utilizar el siguiente comando para forzar el desmontaje:

#fusermount -u -z /mnt/serverB

#Si aún así tienes problemas para desmontar la unidad, es posible que haya algún proceso en ejecución que esté utilizando la unidad. Puedes utilizar el comando fuser para ver qué procesos están utilizando la unidad:

#fuser -vm /mnt/serverB
#kill <PID1> <PID2> <PID3> ...


#MONTAR DIRECOTORIO COMPARTIOD EN UNA CARPETA LOCAL

#PRUBA DE SINCRONIZACIÓN
#sshpass -p 'r0m4n0s.1507' rsync -avz -e "ssh -o StrictHostKeyChecking=no" --delete root@192.168.1.7:/mnt/Impresiones/2023 /mnt/serverB/

#contrab 
#ejecutar un script cada 8 horas a partir de las 8:00 a.m., puede utilizar el siguiente patrón:
#0 8-23/8 * * * python3 /home/soporte/Desktop/bot/sync.py


from datetime import datetime
import smtplib
import os
# Importación de la biblioteca necesaria para enviar correos

import smtplib

# Obtener la fecha y hora actual en el formato "dd/mm/yyyy hh:mm:ss"
current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Configuración del servidor SMTP
smtp_server = "CORREO"
smtp_port = 587
smtp_username = "USUARIO"
smtp_password = "CONTRASEÑA"

# Función para enviar el correo de sincronización
def send_sync_email(to_email, subject, body):
    # Creación del mensaje del correo
    message = f"Subject: {subject}\n\n{body}".encode("utf-8")
    # Conexión al servidor SMTP y envío del correo
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(smtp_username, to_email, message)
    server.quit()


# Agregar la fecha y hora al mensaje del correo
subject = f"Sincronización completada - Respaldo ({current_time})"
body = f"La sincronización entre el servidor IMPRESIONES y el servidor BACKUP se completó con éxito en {current_time}."

# Sincronización de la carpeta del servidor A con la carpeta del servidor BW
exit_code = os.system("sshpass -p 'INGRESATUPASSWORD' rsync -avz -e 'ssh -o StrictHostKeyChecking=no' --delete root@192.168.1.X:/RUTA/DEL/FICHERO/REMOTO /mnt/serverB/")

# Si la sincronización se realizó correctamente
if exit_code == 0:
    # Envío del correo de sincronización
    send_sync_email("INGRESATUCORRE@AQUI.COM",subject, body)

# Si hubo un error durante la sincronización
else:
    # Envío del correo de error
    send_sync_email("INGRESATUCORRE@AQUI.COM", "Sync error", "There was an error while syncing between server A and server B.")