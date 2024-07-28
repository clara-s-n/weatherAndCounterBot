from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from weatherService import get_clima
from aiService import get_ai_response

contador = 0

keyboard = [
        [
            InlineKeyboardButton("Clima", callback_data='clima'),
            InlineKeyboardButton("Contador", callback_data='contador'),
            InlineKeyboardButton("AI", callback_data='ai')
        ]
    ]

async def start(update: Update, context: CallbackContext) -> None:
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Hola! Soy tu bot de clima, contador y AI. Elige una opción:', reply_markup=reply_markup)

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

    elif query.data == 'ai':
        await query.message.reply_text(text="Por favor, ingresa tu consulta para AI:")

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if 'clima' in context.user_data:
        context.user_data.pop('clima')
        clima_info = await get_clima(text)
        await update.message.reply_text(clima_info)
    elif 'ai' in context.user_data:
        context.user_data.pop('ai')
        ai_response = await get_ai_response(text)
        await update.message.reply_text(ai_response)
    else:
        await update.message.reply_text("No se reconoce el comando. Usa el menú para seleccionar una opción.")

    # Mostrar el menú con botones nuevamente
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Elige una opción:', reply_markup=reply_markup)
