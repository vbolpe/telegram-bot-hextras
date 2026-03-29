# dependencies
import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# local
from database.db import init_db
from handlers.help import help_command
from handlers.menu_router import menu_route
from conversations.newh_conv import register_handler_nh
from conversations.register_user import register_handler
from conversations.csv_conv import csv_handler
from conversations.register_client import register_handler_cl
from handlers.start import start_command


# Logging básico 
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# load environment variables
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("No hay token cargado")

def main():
    init_db() #initialize the database

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(register_handler)    # /registrar
    app.add_handler(register_handler_nh) # /horaextra
    app.add_handler(register_handler_cl) # /client
    app.add_handler(csv_handler)         # /csv 

    # Comandos simples
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    # Mensajes de texto (menú)
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu_route
        )
    )

    # Mensaje no reconocido
    async def unknown_text(update, contex):
        await update.message.reply_text(
            "No entendi el mensaje.\n"
            "Usá /help para ver los comandos disponibles."
        )

    app.add_handler(MessageHandler(filters.COMMAND, unknown_text))

    logger.info("Bot iniciado.")
    #app.add_handler(CommandHandler("cancel", cancel))

    logger.info("Bot iniciado.")
    app.run_polling()

if __name__ == "__main__":
    main()
    