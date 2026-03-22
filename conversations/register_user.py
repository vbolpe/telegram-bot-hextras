from telegram import Update
from telegram.ext import (ConversationHandler, MessageHandler, CommandHandler, ContextTypes, filters)
import re
from datetime import datetime
from database.db import create_user, user_exists

#Estados de la conversacion 
REGISTER_LEGAJO = 1 
REGISTER_NOMBRE = 2 
REGISTER_AREA = 3
REGISTER_JORNADA = 4

async def start_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_exists(user_id):
        await update.message.reply_text("👋 Ya estás registrado.")
        return ConversationHandler.END
    
    await update.message.reply_text(
        "👋 Bienvenido.\nVamos a crear tu usuario.\n\nIngresá tu legajo:"
    )
    return REGISTER_LEGAJO

#Carga legajo y valida
async def legajo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    valida = update.message.text.strip()

    if not valida.isdigit():
        await update.message.reply_text(
            "El legajo debe ser un número entero.\n"
            "Ingresalo nuevamente:"
        )
        return REGISTER_LEGAJO

    context.user_data["legajo"] = valida
    await update.message.reply_text("Nombre y apellido: ")
    return REGISTER_NOMBRE

# Carga el nombre y valida
async def nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    valida = update.message.text.strip()
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"

    if not re.match(patron, valida):
        await update.message.reply_text(
            "El nombre solo puede contener letras y espacios. \n"
            "Ej: Roberto Juaréz"
        )
        return REGISTER_NOMBRE
    
    if len(valida.split()) < 2:
        await update.message.reply_text(
            "Ingresá nombre y apellido. \n"
        )
        return REGISTER_NOMBRE
    
    context.user_data["nombre"] = valida
    await update.message.reply_text("Área: ")
    return REGISTER_AREA

async def area(update: Update,context: ContextTypes.DEFAULT_TYPE):
    valida = update.message.text.strip()

    if not valida.replace(" ", "").isalpha():
        await update.message.reply_text(
            "El área solo puede contener letras y espacios.\n"
            "EJ: Soporte "
        )
        return REGISTER_AREA
    
    context.user_data["area"] = valida
    await update.message.reply_text(
        "Jornada laboral:\n"
        "EJ: Lunes a Viernes 09:00 a 13:00"
    )
    return REGISTER_JORNADA

async def jornada(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    valida = update.message.text.strip()

    patron = (
        r"^(Lunes|Martes|Miércoles|Miercoles|Jueves|Viernes|Sábado|Sabado|Domingo)"
        r"\s+a\s+"
        r"(Lunes|Martes|Miércoles|Miercoles|Jueves|Viernes|Sábado|Sabado|Domingo)"
        r"\s+"
        r"([0-2]\d:[0-5]\d)"
        r"\s+a\s+"
        r"([0-2]\d:[0-5]\d)$"
    )

    match = re.match(patron, valida, re.IGNORECASE)

    if not match:
        await update.message.reply_text(
            "Formato inválido.\n"
            "Usá el formato: \n"
            "Lunes a Viernes 12:00 a 18:00"
        )
        return REGISTER_JORNADA
    
    hora_inicio = datetime.strptime(match.group(3), "%H:%M")
    hora_fin = datetime.strptime(match.group(4), "%H:%M")

    if hora_inicio >= hora_fin:
        await update.message.reply_text(
            " La hora de inicio debe ser menor a la hora de fin."
        )
        return REGISTER_JORNADA

    context.user_data["jornada"] = valida

    create_user(
        telegram_id=update.effective_user.id,
        legajo=context.user_data["legajo"],
        nombre=context.user_data["nombre"],
        area=context.user_data["area"],
        jornada=context.user_data["jornada"]
    )

    context.user_data.clear()
    await update.message.reply_text(" Registro completado.")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Carga cancelada.")
    return ConversationHandler.END

# Entry point es /registrar 
register_handler = ConversationHandler(
    entry_points = [CommandHandler("registrar", start_register)],
    states={
      REGISTER_LEGAJO: [MessageHandler(filters.TEXT & ~filters.COMMAND, legajo)],
      REGISTER_NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, nombre)],
      REGISTER_AREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, area)],
      REGISTER_JORNADA: [MessageHandler(filters.TEXT & ~filters.COMMAND, jornada)],
  
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)