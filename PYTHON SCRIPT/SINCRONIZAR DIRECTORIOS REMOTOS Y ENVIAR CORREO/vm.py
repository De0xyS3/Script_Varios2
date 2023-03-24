from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import atexit
import ssl

# Configuración de conexión
host = "nombre_del_host_o_ip"
user = "nombre_de_usuario"
password = "contraseña"
port = 443

# ID del contenedor a hacer backup
container_id = "ID_del_contenedor"

# Ruta de destino del backup
backup_destination = "/ruta/de/destino"

# Conexión al servidor VMware
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_NONE
si = SmartConnect(host=host, user=user, pwd=password, port=port, sslContext=context)
atexit.register(Disconnect, si)

# Buscar el contenedor por ID
content = si.RetrieveContent()
container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
vm = container.view.get_by_id(container_id)

# Crear el objeto de especificaciones de backup
spec = vim.vm.BackupManager.BackupSpec()
spec.destinationUri = backup_destination

# Iniciar el backup
backup_manager = content.backupManager
task = backup_manager.Backup(vm, spec)
