import json
import openai
from openai import OpenAI

# Cargar configuración
with open('configuration\\appsettings.json') as config_file:
    config = json.load(config_file)

OPENAI_API_KEY = config['OpenAiApiKey']

client = OpenAI(api_key=OPENAI_API_KEY)

async def get_ai_response(prompt: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

