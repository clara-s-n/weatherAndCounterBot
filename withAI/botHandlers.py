from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from weatherService import get_climate
from aiService import get_ai_response

contador = 0

keyboard = [
    [
        InlineKeyboardButton("Clima", callback_data='clima'),
        InlineKeyboardButton("Contador", callback_data='contador'),
        InlineKeyboardButton("AI", callback_data='ai')
    ],
    [
        InlineKeyboardButton("Salir", callback_data='salir')
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
        context.user_data['awaiting_clima'] = True
        await query.message.reply_text(text="Por favor, ingresa el nombre de la ciudad para obtener el clima:")
    elif query.data == 'contador':
        contador += 1
        await query.message.reply_text(text=f"Contador: {contador}")
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text('Elige una opción:', reply_markup=reply_markup)
        
    elif query.data == 'ai':
        context.user_data['awaiting_ai'] = True
        await query.message.reply_text(text="Por favor, ingresa tu consulta para AI:")
    elif query.data == 'salir':
        await query.message.reply_text(text="El bot se está cerrando. ¡Adiós!")
        await context.application.stop()

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if context.user_data.get('awaiting_clima'):
        context.user_data.pop('awaiting_clima')
        clima_info = await get_climate(text)
        await update.message.reply_text(clima_info)
    elif context.user_data.get('awaiting_ai'):
        context.user_data.pop('awaiting_ai')
        ai_response = await get_ai_response(text)
        await update.message.reply_text(ai_response)
    else:
        await update.message.reply_text("No se reconoce el comando. Usa el menú para seleccionar una opción.")
    
    # Mostrar el menú con botones nuevamente
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Elige una opción:', reply_markup=reply_markup)


