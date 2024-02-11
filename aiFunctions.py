import aiohttp
import constants
import json
import streamlit as st

api_key = st.secrets["openaikey"]


def parse_content_to_json(content):
    json_part = content.replace('```json\n', '').replace('```', '')
    json_object = json.loads(json_part)
    return json_object


async def scan_image(image_content):
    try:
        async with aiohttp.ClientSession() as session:
            user_message_content = [{'type': 'text', 'text': 'Give me a json object of the publicity, the response '
                                                             'wil be directly process as a JSON.'},
                                    {'type': 'image_url',
                                     'image_url': {'url': f"data:image/jpeg;base64,{image_content}"}}]

            payload = {
                'model': 'gpt-4-vision-preview',
                'max_tokens': 4096,
                'messages': [
                    {'role': 'system', 'content': constants.IMAGE_SYST_PROMPT},
                    {'role': 'user', 'content': user_message_content}
                ]
            }

            headers = {'Authorization': f'Bearer {api_key}'}
            async with session.post('https://api.openai.com/v1/chat/completions', json=payload,
                                    headers=headers) as response:
                response_text = await response.text()
                response_data = json.loads(response_text)
                if 'choices' in response_data:
                    return parse_content_to_json(response_data['choices'][0]['message']['content'])
                else:
                    print("API response:", response_data)
                    return None
    except Exception as error:
        print("Error processing chat:", error)
        print("result ", response_data['choices'][0]['message']['content'])
