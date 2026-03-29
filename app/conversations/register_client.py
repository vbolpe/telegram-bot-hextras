from telegram import Update
from telegram.ext import (ConversationHandler, MessageHandler, CommandHandler, ContextTypes, filters)
import re
from database.db import user_exists, create_client, client_exists
 
# Estados de la conversacion
REGISTER_CLIENT = 1
 
async def start_register_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
 
    if not user_exists(user_id):
        await update.message.reply_text("Debe tener un usuario antes de cargar un cliente.")
        return ConversationHandler.END
 
    await update.message.reply_text("Iniciemos con el alta del cliente.\nIngrese el nombre del cliente:")
    return REGISTER_CLIENT
 
 
async def client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    valida = update.message.text.strip()
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"
 
    if not re.match(patron, valida):
        await update.message.reply_text(
            "El nombre solo puede contener letras y espacios.\n"
            "Ej: Roberto Juárez"
        )
        return REGISTER_CLIENT
 
    if client_exists(valida):
        await update.message.reply_text("El cliente ya está cargado.")
        return ConversationHandler.END
 
    create_client(nombre=valida)
 
    await update.message.reply_text("✅ Cliente cargado con éxito.")
    return ConversationHandler.END
 
 
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Carga cancelada.")
    return ConversationHandler.END
 
 
# Entry point es /client
register_handler_cl = ConversationHandler(
    entry_points=[CommandHandler("client", start_register_client)],
    states={
        REGISTER_CLIENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, client)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)