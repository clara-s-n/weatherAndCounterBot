import json
import requests

# Cargar configuración
with open('configuration\\appsettings.json') as config_file:
    config = json.load(config_file)

OPENWEATHERMAP_API_KEY = config['OpenWeatherMapApiKey']

async def get_climate(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=es"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"El clima en {city} es {description} con una temperatura de {temp}°C."
    else:
        return "Lo siento, no pude obtener el clima para esa ciudad."
