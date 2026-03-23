from telegram import (Update, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (ConversationHandler, MessageHandler, CommandHandler, ContextTypes, filters)
import re
from datetime import datetime
from database.db import user_exists, get_clientes, overtime_works

#Estados de la conversacion 
REGISTER_FECHA =  1
REGISTER_HORA_I = 2
REGISTER_HORA_F = 3
REGISTER_DESCRI = 4
REGISTER_TICKET = 5
REGISTER_CLIENT = 6

async def start_hora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id =  update.effective_user.id

    if not user_exists(user_id):
        await update.message.reply_text("No esta registrado.\n Usá /start para registrate")
        return ConversationHandler.END
    
    await update.message.reply_text(
        " Bienvenido.\nVamos a carga tus horas extras.\n\n"
        "Ingresá la fecha (DD/MM/AAAA):"
    )
    return REGISTER_FECHA

#Carga y valida fecha 

async def fecha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()

    try:
        fecha_valida = datetime.strptime(texto, "%d/%m/%Y")
    except ValueError:
        await update.message.reply_text(
            "Fecha inválida.\nUsá el formato DD/MM/AAAA"
        )
        return REGISTER_FECHA

    context.user_data["fecha"] = texto
    await update.message.reply_text("Hora de inicio (HH:MM):")
    return REGISTER_HORA_I

#Carga Inicio de Hora extra y texto 

async def incio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()

    try:
        hora = datetime.strptime(texto, "%H:%M")
    except ValueError:
        await update.message.reply_text(
            "Hora inválida.\nFormato correcto: 12:00"
        )
        return REGISTER_HORA_I

    context.user_data["hora_inicio"] = texto
    await update.message.reply_text("Hora de finalización (HH:MM):")
    return REGISTER_HORA_F

async def fin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()

    try:
        hora_fin = datetime.strptime(texto, "%H:%M")
        hora_inicio = datetime.strptime(
            context.user_data["hora_inicio"], "%H:%M"
        )
    except ValueError:
        await update.message.reply_text(
            "Hora inválida.\nFormato correcto: 12:00"
        )
        return REGISTER_HORA_F

    if hora_fin <= hora_inicio:
        await update.message.reply_text(
            "La hora de fin debe ser mayor a la de inicio."
        )
        return REGISTER_HORA_F

    context.user_data["hora_fin"] = texto
    await update.message.reply_text("Descripción de la tarea:")
    return REGISTER_DESCRI


async def descr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()

    if len(texto.split()) < 2:
        await update.message.reply_text(
            "Ingrese la descripcion de la tarea. \n"
            "NICOLAS DEJA DE TRATAR DE ROMPER LA DB LRCCDCDTH"
        )
        return REGISTER_DESCRI

    context.user_data["descri"] = update.message.text
    await update.message.reply_text("Número de ticket (ej: DND-43333):")
    return REGISTER_TICKET

async def tick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    #patron = r"^DND-\d+$"

    if not re.match(r"^DND-\d+$", texto):
        await update.message.reply_text(
            "Formato inválido \nEjemplo: DND-43333"
            )
        return REGISTER_TICKET
    
    context.user_data["ticket"] = texto

    clientes = get_clientes()

    keyboard = [[c] for c in clientes]
    keyboard.append(["Cancelar"])
    await update.message.reply_text(
        "Seleccioná el cliente:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    ) 
    return REGISTER_CLIENT

async def client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()

    if texto == "Cancelar":
        context.user_data.clear()
        await update.message.reply_text(
            "Carga cancelada.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    clientes = get_clientes()

    if texto not in clientes:
        await update.message.reply_text(
            "Cliente inválido.\nSeleccioná uno de la lista."
        )
        return REGISTER_CLIENT

    context.user_data["cliente"] = texto

    overtime_works(
        telegram_id=update.effective_user.id,
        fecha=context.user_data["fecha"],
        hora_inicio=context.user_data["hora_inicio"],
        hora_fin=context.user_data["hora_fin"],
        descripcion=context.user_data["descri"],
        ticket=context.user_data["ticket"],
        cliente=context.user_data["cliente"],
    )
    
    context.user_data.clear()

    await update.message.reply_text(
        "Hora extra cargada correctamente.",
        reply_markup=ReplyKeyboardRemove()
    )

    # acá después guardás en DB
    return ConversationHandler.END



 # Cancelar en cualquier momento
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Operación cancelada.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

register_handler_nh = ConversationHandler(
    entry_points = [CommandHandler("horaextra", start_hora)],
    states={
      REGISTER_FECHA: [MessageHandler(filters.TEXT & ~filters.COMMAND, fecha)],
      REGISTER_HORA_I: [MessageHandler(filters.TEXT & ~filters.COMMAND, incio)],
      REGISTER_HORA_F: [MessageHandler(filters.TEXT & ~filters.COMMAND, fin)],
      REGISTER_DESCRI: [MessageHandler(filters.TEXT & ~filters.COMMAND, descr)],
      REGISTER_TICKET: [MessageHandler(filters.TEXT & ~filters.COMMAND, tick)],
      REGISTER_CLIENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, client)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
