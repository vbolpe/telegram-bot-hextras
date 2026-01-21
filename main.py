import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from database.db import init_db
from conversations.register_user import register_handler

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN no definido")


def main():
    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    # Conversations primero
    app.add_handler(register_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
