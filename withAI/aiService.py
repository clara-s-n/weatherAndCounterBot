import json
import openai

# Cargar configuración
with open('settings.json') as config_file:
    config = json.load(config_file)

OPENAI_API_KEY = config['OpenAiApiKey']

openai.api_key = OPENAI_API_KEY

async def get_ai_response(prompt: str) -> str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()
