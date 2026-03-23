from telegram import ReplyKeyboardMarkup

def main_menu():
    keyboard=[
        ["Cargar hora extra"],
        ["Descargar CSV"],
        ["Cargar cliente"],
        ["Ayuda"],
        ["Cancelar"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )