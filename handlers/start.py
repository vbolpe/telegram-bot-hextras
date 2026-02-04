from telegram import Update
from telegram.ext import ContextTypes
from database.db import user_exists
from handlers.menu import main_menu

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    welcome_text = ""
    if not user_exists(user_id):

        update.message.text = "__REGISTER__"
        welcome_text = (
            "¡Hola! 👋 Bienvenido al bot de gestión de horas extra.\n\n"
            "Vamos a crear tu usuario para empezar a cargar tus horas:\n"
            "Tene a mano tu numero de legajo.\n Usá /start"
        )
        return await context.application.process_update(update)
    
    welcome_text = (
        "¡Hola! 👋 Bienvenido al bot de gestión de horas extra.\n\n"
        "Seleccioná una opción:\n"
        
    )
    await update.message.reply_text(welcome_text, reply_matkup=main_menu())