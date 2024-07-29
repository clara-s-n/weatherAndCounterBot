import json
from openai import OpenAI
from openai import RateLimitError, OpenAIError

# Cargar configuración
with open('configuration\\appsettings.json') as config_file:
    config = json.load(config_file)

OPENAI_API_KEY = config['OpenAiApiKey']

client = OpenAI(api_key=OPENAI_API_KEY)

async def get_ai_response(prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message['content']
    except RateLimitError:
        return "Se ha alcanzado el límite de mensajes. Inténtalo más tarde."
    except OpenAIError as e:
        return f"Error en el servicio de OpenAI: {str(e)}"


