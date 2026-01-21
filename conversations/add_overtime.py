from telegram import Update
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

OT_DATE = 10
OT_START = 11
OT_END = 12
OT_DESC = 13
OT_TICKET = 14
OT_CLIENT = 15

async def start_overtime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📅 Fecha (YYYY-MM-DD):")
    return OT_DATE

async def ot_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["fecha"] = update.message.text
    await update.message.reply_text("⏰ Hora inicio:")
    return OT_START

async def ot_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["inicio"] = update.message.text
    await update.message.reply_text("⏰ Hora fin:")
    return OT_END

async def ot_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["fin"] = update.message.text
    await update.message.reply_text("📝 Descripción:")
    return OT_DESC

async def ot_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["desc"] = update.message.text
    await update.message.reply_text("🎫 Ticket:")
    return OT_TICKET

async def ot_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ticket"] = update.message.text
    await update.message.reply_text("🏢 Cliente:")
    return OT_CLIENT

async def ot_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["cliente"] = update.message.text

    # TODO: guardar en DB

    await update.message.reply_text("✅ Hora extra registrada.")
    return ConversationHandler.END

overtime_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_overtime, pattern="extra")
    ],
    states={
        OT_DATE: [MessageHandler(filters.TEXT, ot_date)],
        OT_START: [MessageHandler(filters.TEXT, ot_start)],
        OT_END: [MessageHandler(filters.TEXT, ot_end)],
        OT_DESC: [MessageHandler(filters.TEXT, ot_desc)],
        OT_TICKET: [MessageHandler(filters.TEXT, ot_ticket)],
        OT_CLIENT: [MessageHandler(filters.TEXT, ot_client)],
    },
    fallbacks=[]
)
