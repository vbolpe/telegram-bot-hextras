from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    keyboard = [
        [InlineKeyboardButton("➕ Nueva hora extra", callback_data="ADD_OT")],
        [InlineKeyboardButton("📊 Ver horas del mes", callback_data="VIEW_OT")],
        [InlineKeyboardButton("⬇️ Descargar CSV", callback_data="CSV_OT")]
    ]
    return InlineKeyboardMarkup(keyboard)
