from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from handlers.menu import main_menu
from conversations.newh_conv import start_hora
from conversations.csv_conv import start_csv

async def menu_route(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Cargar hora extra":
        return await start_hora(update, context)
 
    if text == "Descargar CSV":
        return await start_csv(update, context)
 
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
    
    await update.message.reply_text(
        "No entendí el mensaje. Usá el menú ",
        reply_markup=main_menu()
    )