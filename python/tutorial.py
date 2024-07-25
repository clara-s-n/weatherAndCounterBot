import logging
from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# API Keys
TELEGRAM_API_TOKEN = '7180453469:AAFYOr6ryUtGzCaMWPj9UBwmP1q8bSekpeA'
OPENWEATHERMAP_API_KEY = 'f7ee555c739dca55cb2f9a2538b0f180'

# Contador global
contador = 0

# Funciones de comandos
async def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['Clima', 'Contador']]
    await update.message.reply_text(
        'Hola! Soy tu bot de clima y contador. Elige una opción:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

async def clima(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Por favor, ingresa el nombre de la ciudad para obtener el clima:')

async def get_clima(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=es"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"El clima en {city} es {description} con una temperatura de {temp}°C."
    else:
        return "Lo siento, no pude obtener el clima para esa ciudad."

async def handle_message(update: Update, context: CallbackContext) -> None:
    global contador
    text = update.message.text

    if text.lower() == 'clima':
        await clima(update, context)
    elif text.lower() == 'contador':
        contador += 1
        await update.message.reply_text(f"Contador: {contador}")
    else:
        clima_info = await get_clima(text)
        await update.message.reply_text(clima_info)

# Configuración principal
def main() -> None:
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
