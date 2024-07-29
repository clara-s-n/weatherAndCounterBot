# Weather, Counter, and AI Telegram Bot

Este bot de Telegram proporciona información sobre el clima, un contador simple y respuestas generadas por inteligencia artificial. Está desarrollado en Python utilizando la librería `python-telegram-bot` y la API de OpenAI.

## Requisitos

- Python 3.12+
- Una cuenta de OpenAI con una API key
- Un bot de Telegram con su API key
- Una cuenta de OpenWeather con su API key

## Instalación

1. Clona el repositorio o descarga los archivos.

2. Crea un entorno virtual y actívalo:
   ```sh
   python -m venv venv
   source venv/bin/activate # En Windows usa `venv\Scripts\activate`
   ```
   
3. Instala las dependencias
   ```sh
    pip install -r requirements.txt
   ```
   
4. Configura las claves de las API en un archivo 'appsettings.json' dentro del directorio 'configuration'

## Uso
1. Ejecuta el bot
   ```sh
   # Solamente el bot de clima y contador
    python justTheBot/main.py
   ```

   ```sh
   # La versión con AI
   python withAI/main.py
   ```
2. Interactua con tu bot en Telegram utilizando los comandos y botones proporcionados

## Estructura del Proyecto
- main.py: Configuración y ejecución principal del bot.
- botHandlers.py: Define los manejadores de comandos y mensajes del bot.
- weatherService.py: Servicio para obtener información sobre el clima.
- aiService.py: Servicio para obtener respuestas de AI desde OpenAI.
- configuration/appsettings.json: Archivo de configuración para las claves de API.

## Funcionalidades
### Clima
Envía el nombre de una ciudad para obtener información meteorológica.

### Contador
Un contador simple que incrementa cada vez que se selecciona la opción.

### AI
Envía una consulta para recibir una respuesta generada por inteligencia artificial.

### Salir
Cierra el bot.

## Ejemplo de Interacción
- Inicia el bot con /start.
- Usa los botones para seleccionar una opción.
- Envía la información necesaria según la opción seleccionada.
- Recibe la respuesta del bot y elige una nueva opción o cierra el bot.
