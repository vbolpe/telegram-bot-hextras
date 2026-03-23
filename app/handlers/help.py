from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 *Comandos disponibles:*\n\n"
        "/start - Iniciar el bot\n"
        "/Crear usuario - Debe ingresar el legajo como numero y el resto en texto\n"
        "/pasar hora - Formato de fecha: DD-MM-AAAA y las horas en HH:MM\n"
        "/help - Mostrar este mensaje de ayuda\n\n"
        "Para cualquier duda o problema, contacta al administrador."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

