from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from weatherService import get_climate

contador = 0

keyboard = [
        [
            InlineKeyboardButton("Clima", callback_data='clima'),
            InlineKeyboardButton("Contador", callback_data='contador')
        ]
    ]

async def start(update: Update, context: CallbackContext) -> None:
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Hola! Soy tu bot de clima y contador. Elige una opción:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    global contador
    if query.data == 'clima':
        await query.message.reply_text(text="Por favor, ingresa el nombre de la ciudad para obtener el clima:")
    elif query.data == 'contador':
        contador += 1
        await query.message.reply_text(text=f"Contador: {contador}")
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text('Elige una opción:', reply_markup=reply_markup)
    

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    clima_info = await get_climate(text)
    await update.message.reply_text(clima_info)
    
    # Mostrar el menú con botones nuevamente
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Elige una opción:', reply_markup=reply_markup)
