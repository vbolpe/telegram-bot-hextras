# dependencies
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# local
from database.db import init_db
from handlers.help import help_command
# from handlers.cancel import cancel
from handlers.menu_router import menu_route
from conversations.newh_conv import register_handler_nh
from conversations.register_user import register_handler
from conversations.csv_conv import csv_handler
from handlers.start import start_command

# load environment variables
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("No hay token cargado")

def main():
    init_db() #initialize the database

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(register_handler)
    app.add_handler(register_handler_nh)
    app.add_handler(csv_handler)
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu_route
        )
    )
    app.add_handler(CommandHandler("help", help_command))
    #app.add_handler(CommandHandler("cancel", cancel))

    # Mando lo que se le canto 

    async def unknown_text(update, contex):
        await update.message.reply_text(
            "No entendi el mensaje.\n"
            "Usá /help para ver los comandos disponibles."
        )
    app.run_polling()

if __name__ == "__main__":
    main()
    