from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler


async def menu_route(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Cargar hora extra":
        await update.message.reply_text(
            "Iniciando carga de hora extra...",
            reply_markup=ReplyKeyboardRemove()
        )
        return await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="/horaextra"
)
    
    if text == "Descargar CSV":
        await update.message.reply_text(
            "Generación de CSV por mes",
            reply_markup=ReplyKeyboardRemove()
        )
        
        await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="/csv"
)
    
    if text == "Ayuda":
        await update.message.reply_text(
            "Usá el menú para navegar o /help ."
        )
        return
    if text == "Cancelar":
        context.user_data.clear()
        await update.message.reply_text(
            "Operación cancelada.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    
    return