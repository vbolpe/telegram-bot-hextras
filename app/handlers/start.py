from telegram import Update
from telegram.ext import ContextTypes
from database.db import user_exists
from handlers.menu import main_menu

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not user_exists(user_id):
        await update.message.reply_text(
            "¡Hola! 👋 Bienvenido al bot de gestión de horas extra.\n\n"
            "Vamos a crear tu usuario para empezar a cargar tus horas.\n"
            "Tené a mano tu número de legajo.\n\n"
            "Usá el menú para continuar 👇",
        )
        return

    await update.message.reply_text(
        "¡Hola! 👋 Bienvenido al bot de gestión de horas extra.\n\n"
        "Seleccioná una opción 👇",
        reply_markup=main_menu()
    )
