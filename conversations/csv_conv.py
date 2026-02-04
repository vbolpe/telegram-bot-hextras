from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, ContextTypes, filters
from datetime import datetime
import csv
import os

from database.db import user_exists, get_overtime_by_moth

REGISTER_MES = 1

async def start_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not user_exists(user_id):
        await update.message.reply_text(
            "No estás registrado. \nUsá /start para registrarte."
        )
        return ConversationHandler.END
    
    await update.message.reply_text(
        "Ingresá el mes a consultar. \n"
        "Formato: MM/YYYY\n"
        "Ejemplo: 01/2026"
    )
    return REGISTER_MES

async def mes_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()

    try:
        fecha = datetime.strptime(texto, "%m%Y")
    except ValueError:
        await update.message.reply_text(
            "Formato inválido.\nUsá MM/YYYY"
        )
        return REGISTER_MES
    
    year = fecha.year
    month = fecha.month
    user_id = update.effective_user.id

    registros = get_overtime_by_moth(user_id, year, month)

    if not registros:
        await update.message.reply_text(
            "No se relizaron horas extras en ese mes."
        )
        return CommandHandler.END
    
    fechas = sorted(set(r[0] for r in registros))

    resumen = "\n".join(
        f"{f} se realizaron horas" for f in fechas
    )

    await update.message.reply_text(
        "Resumen del mes: \n\n" + resumen
    )

    filename = f"horas_extras_{month:02d}_{year}.csv"
    filepath = f"/tmp/{filename}"

    with open(filepath, mode="w", newline ="", encoding="uft-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Fecha", "Hora Inicio", "Hora Fin", "Descripción", "Ticket", "Cliente"
        ])
        for r in registros:
            writer.writerow(r)

    ## Enviar Archivo ##
    with open(filepath, "rb") as file:
        await update.message.reply_document(
            document=file,
            filename=filename
        )
    os.remove(filepath)

    return ConversationHandler.END

csv_handler = ConversationHandler(
    entry_points=[CommandHandler("csv", start_csv)],
    states={
        REGISTER_MES: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, mes_csv)
        ],
    },
    fallbacks=[],
)