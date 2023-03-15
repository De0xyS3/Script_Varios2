from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import ssl
import atexit
import datetime
import tarfile
import paramiko

# Configuración de conexión SSH
SSH_USER="usuario"  # Reemplazar con el nombre de usuario con acceso SSH
SSH_HOST="192.168.1.100"  # Reemplazar con la dirección IP del servidor VMware ESXi
SSH_KEY="/ruta/a/llave/ssh"  # Reemplazar con la ruta a la llave SSH

# Configuración de backup
BACKUP_DIR="/ruta/a/carpeta/backup"  # Reemplazar con la ruta a la carpeta donde se guardarán los archivos de backup

# Conexión SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(SSH_HOST, username=SSH_USER, key_filename=SSH_KEY)

# Conexión al servidor VMware ESXi
s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE
si = SmartConnectNoSSL(host=SSH_HOST, user="root", pwd="password", sslContext=s)
atexit.register(Disconnect, si)

# Obtener lista de máquinas virtuales
content = si.RetrieveContent()
vm_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
vm_data = vm_list.view

# Iterar sobre las máquinas virtuales y hacer backup
for vm in vm_data:
    print("Haciendo backup de máquina virtual %s (ID: %s)..." % (vm.name, vm._moId))

    # Obtener archivo de configuración de la máquina virtual
    vm_conf = vm.config.files.vmPathName

    # Crear archivo de backup
    backup_filename = "%s-%s.tar.gz" % (vm.name, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    backup_file = tarfile.open(backup_filename, "w:gz")
    backup_file.add(vm_conf)
    backup_file.close()

    # Enviar archivo de backup por SSH
    ssh_transport = ssh.get_transport()
    ssh_sftp = ssh_transport.open_sftp()
    ssh_sftp.put(backup_filename, BACKUP_DIR + "/" + backup_filename)
    ssh_sftp.close()

    print("Backup guardado en %s/%s" % (BACKUP_DIR, backup_filename))

# Cerrar conexión SSH
ssh.close()
