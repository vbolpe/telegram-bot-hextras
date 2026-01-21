from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database.db import user_exists

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not user_exists(user_id):
        # Disparador interno para el ConversationHandler
        update.message.text = "__REGISTER__"
        return await context.application.process_update(update)

    await update.message.reply_text("👋 Bienvenido nuevamente")

start_handler = CommandHandler("start", start)
