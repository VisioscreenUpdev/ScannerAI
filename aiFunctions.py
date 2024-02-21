import aiohttp
import constants
import json
import streamlit as st
import asyncio


api_key = st.secrets["openaikey"]


def parse_content_to_json(content):
    json_part = content.replace('```json\n', '').replace('```', '')
    json_object = json.loads(json_part)
    return json_object


async def scan_image(image_content):
    retry_delay = 5  # seconds to wait before retrying
    max_retries = 5  # maximum number of retries
    try_count = 0

    while try_count < max_retries:
        try:
            async with aiohttp.ClientSession() as session:
                user_message_content = [
                    {'type': 'text', 'text': 'Give me a json object of the publicity, the response will be directly process as a JSON.'},
                    {'type': 'image_url', 'image_url': {'url': f"data:image/jpeg;base64,{image_content}"}}
                ]

                payload = {
                    'model': 'gpt-4-vision-preview',
                    "temperature": 0,
                    'max_tokens': 4096,
                    'messages': [
                        {'role': 'system', 'content': constants.IMAGE_SYST_PROMPT},  # Remplacez 'IMAGE_SYST_PROMPT' par la constante appropriée
                        {'role': 'user', 'content': user_message_content}
                    ]
                }

                headers = {'Authorization': f'Bearer {api_key}'}
                async with session.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers) as response:
                    response_text = await response.text()
                    response_data = json.loads(response_text)
                    if 'choices' in response_data:
                        return parse_content_to_json(response_data['choices'][0]['message']['content'])  # ou votre fonction parse_content_to_json
                    else:
                        print("API response:", response_data)
                        raise Exception("rate_limit_exceeded")
        except Exception as error:
            print("Error processing chat:", error)
            if 'rate_limit_exceeded' in str(error):  # Vous devriez affiner cette vérification en fonction de la structure réelle de l'erreur
                print(f"Rate limit exceeded, retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                try_count += 1
            else:
                raise  # relance l'exception si ce n'est pas une erreur de limite de taux

        # En cas d'erreur de limite de taux, augmentez le délai d'attente pour le prochain essai
        retry_delay += 4

    print("Max retries exceeded.")
    return None

