from telegram import Update
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
from database.db import user_exists, create_user

REGISTER_LEGAJO = 1
REGISTER_NOMBRE = 2
REGISTER_AREA = 3
REGISTER_JORNADA = 4


async def start_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_exists(user_id):
        await update.message.reply_text("👋 Ya estás registrado.")
        return ConversationHandler.END

    await update.message.reply_text(
        "👋 Bienvenido.\nVamos a crear tu usuario.\n\nIngresá tu legajo:"
    )
    return REGISTER_LEGAJO


async def legajo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["legajo"] = update.message.text
    await update.message.reply_text("Nombre y apellido:")
    return REGISTER_NOMBRE


async def nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["nombre"] = update.message.text
    await update.message.reply_text("Área:")
    return REGISTER_AREA


async def area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["area"] = update.message.text
    await update.message.reply_text("Jornada laboral:")
    return REGISTER_JORNADA


async def jornada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["jornada"] = update.message.text

    create_user(
        telegram_id=update.effective_user.id,
        legajo=context.user_data["legajo"],
        nombre=context.user_data["nombre"],
        area=context.user_data["area"],
        jornada=context.user_data["jornada"]
    )

    await update.message.reply_text("✅ Usuario registrado correctamente")
    return ConversationHandler.END


register_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_register)],
    states={
        REGISTER_LEGAJO: [MessageHandler(filters.TEXT & ~filters.COMMAND, legajo)],
        REGISTER_NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, nombre)],
        REGISTER_AREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, area)],
        REGISTER_JORNADA: [MessageHandler(filters.TEXT & ~filters.COMMAND, jornada)],
    },
    fallbacks=[],
)
