import logging
import json
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from botHandlers import start, handle_message, button

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Cargar configuración
with open('configuration\\appsettings.json') as config_file:
    config = json.load(config_file)

TELEGRAM_API_TOKEN = config['TelegramApiToken']

# Configuración principal
def main() -> None:
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        application.run_polling()
    except KeyboardInterrupt:
        print("Bot detenido por el usuario")
    finally:
        application.stop()

if __name__ == '__main__':
    main()
