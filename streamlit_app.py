import json
import asyncio
import aiohttp
import streamlit as st
import base64

# Replace with your actual OpenAI API key
api_key = "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"
systPrompt = """
    You will be provided with a picture of a publicity you will need to described the product as the field below, describe it in French. Max 4000 chars.
    {
        Produit: "Description of the product",
        Prix: "The price of the product or offer",
        Compagnie: "Name of the company",
        Couleur: "The principales colors",
        Evenement: "If special event give event name"
    }
"""

async def process_chat(image_content, system_prompt=None, is_url=True):
    try:
        async with aiohttp.ClientSession() as session:
            user_message_content = [
                {'type': 'text', 'text': 'Give me a json object of the publicity'}
            ]

            if is_url:
                user_message_content.append({'type': 'image_url', 'image_url': {'url': image_content}})
            else:
                # Adjusting for base64 image format
                user_message_content.append({'type': 'image_url', 'image_url': {'url': f"data:image/jpeg;base64,{image_content}"}})

            payload = {
                'model': 'gpt-4-vision-preview',
                'max_tokens': 4096,
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_message_content}
                ]
            }

            headers = {'Authorization': f'Bearer {api_key}'}
            async with session.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers) as response:
                response_data = await response.json()
                if 'choices' in response_data:
                    return parse_content_to_json(response_data['choices'][0]['message']['content'])
                else:
                    print("API response:", response_data)
                    return None
    except Exception as error:
        print("Error processing chat:", error)

def parse_content_to_json(content):
    json_part = content.replace('```json\n', '').replace('```', '')
    json_object = json.loads(json_part)
    return json_object

def encode_image_to_base64(uploaded_image):
    return base64.b64encode(uploaded_image.read()).decode()

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state['history'] = []

def display_data():
    st.title("Image Analysis DEMO- Visioscreen")
    url_pub = st.text_input("Enter the URL of the image:")
    uploaded_image = st.file_uploader("Or upload an image (JPEG/PNG)", type=["jpg", "jpeg", "png"])

    if st.button("Analyze Image"):
        if url_pub:
            data = asyncio.run(process_chat(url_pub, systPrompt))
            st.session_state['history'].append(data)
            st.json(data)
        elif uploaded_image:
            base64_image = encode_image_to_base64(uploaded_image)
            data = asyncio.run(process_chat(base64_image, systPrompt, is_url=False))
            st.session_state['history'].append(data)
            st.json(data)
        else:
            st.warning("Please enter a URL or upload an image.")

    if st.session_state['history']:
        st.subheader("Analysis History")
        for idx, history_data in enumerate(st.session_state['history']):
            st.json(history_data)
            if st.button(f"Delete Analysis #{idx + 1}"):
                st.session_state['history'].pop(idx)

if __name__ == '__main__':
    display_data()
