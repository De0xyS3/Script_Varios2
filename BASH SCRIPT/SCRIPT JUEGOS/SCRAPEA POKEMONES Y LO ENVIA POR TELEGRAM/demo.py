import logging
from telegram.ext import Updater, MessageHandler, filters
from queue import Queue

# Habilitar el registro de depuración
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token de tu bot de Telegram
TOKEN = "ID"

# Crea una cola de actualizaciones
update_queue = Queue()

# Función manejadora de mensajes nuevos
def welcome_message(update, context):
    # Comprobar si el mensaje es un mensaje de unión a un grupo
    if update.message.new_chat_members is not None:
        # Enviar un mensaje de bienvenida al grupo
        update.message.reply_text("¡Bienvenido al grupo! Espero que tengas un buen día.")

# Crear el Updater y registrar la función manejadora
updater = Updater(TOKEN, update_queue=update_queue)
dispatcher = updater.dispatcher
welcome_handler = MessageHandler(filters.status_update.new_chat_members, welcome_message)
dispatcher.add_handler(welcome_handler)

# Iniciar el bot
updater.start_polling()
