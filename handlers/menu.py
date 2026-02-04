from telegram import replyKeyboardMarkup

def main_menu():
    keyboard=[
        ["Cargar hora extra"],
        ["Descargar CSV"],
        ["Ayuda"],
        ["Cancelar"]
    ]

    return replyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )