import json
import asyncio

import PyPDF2
import pandas as pd
import PyPDF2
import io
import asyncio
import aiohttp
import streamlit as st
import base64
from pdf2image import convert_from_bytes
import io
import constants

api_key = st.secrets["openaikey"]


def show_tables(json_data):
    """
    Converts a JSON object to a table in Streamlit.

    Parameters:
    - json_data (list of dicts): JSON data to be converted. It should be a list of dictionaries.
    """
    two_price_field = "Prix UNITE 2"
    # Directly convert the list of dictionaries to a pandas DataFrame
    two_prices_items = [item for item in json_data if two_price_field in item]
    one_price_item = [item for item in json_data if two_price_field not in item]

    st.title('Produits à Tarif Unique')
    if len(one_price_item) > 0:
        df = pd.DataFrame(one_price_item)
        st.dataframe(df, width=5500)
    else:
        st.info("Aucun produit à Tarif Unique trouvé")

    st.title('Produits à Deux Tarifs')
    if len(two_prices_items) > 0:
        df = pd.DataFrame(two_prices_items)
        st.dataframe(df, width=5500)
    else:
        st.info("Aucun produit à deux tarifs trouvé")


async def process_chat(image_content, system_prompt=None):
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
                    {'role': 'system', 'content': system_prompt},
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


def parse_content_to_json(content):
    json_part = content.replace('```json\n', '').replace('```', '')
    json_object = json.loads(json_part)
    return json_object


def encode_image_to_base64(image):
    # Assuming image is a PIL image; convert it to bytes in base64 for web display or further processing
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()



# def display_data():
#     st.title("Scanner IA by VisioScreen")
#     uploaded_pdf = st.file_uploader("Veuillez importer un PDF", type=["pdf"])
#     if uploaded_pdf:
#         pdf_bytes = uploaded_pdf.read()  # Read PDF bytes once
#
#         try:
#             # Use PdfReader to open the PDF
#             reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
#             max_page_num = len(reader.pages)  # Get the number of pages
#         except Exception as e:
#             st.error(f"Failed to process the PDF. Please ensure it is a valid file. Error: {e}")
#             return
#
#         page_num = st.number_input("Enter the page number to analyze", value=0, step=1, format="%d")
#
#         if st.button("Analyze PDF") and page_num <= max_page_num:
#             st.info(page_num)
#             try:
#                 # Convert only the selected page to an image
#                 pdf_image = convert_from_bytes(pdf_bytes, first_page=page_num, last_page=page_num)[0]
#                 base64_image = encode_image_to_base64(pdf_image)
#                 with st.spinner('Analyse de la page avec IA'):
#                     # Process the image as before
#                     # Assume process_chat and constants.SYST_PROMPT are defined elsewhere
#                     data = asyncio.run(process_chat(base64_image, constants.SYST_PROMPT))
#                     st.json(data)  # Display the JSON response
#                     # Assume show_tables is defined elsewhere and displays data in a table format
#                     show_tables(data)
#             except Exception as e:
#                 st.error(f"Error processing the PDF page: {e}")
#     else:
#         st.warning("Veuillez importer un PDF")
def display_data():
    st.title("Scanner IA by VisioScreen")
    uploaded_pdf = st.file_uploader("Veuillez importer un PDF", type=["pdf"])
    if uploaded_pdf:
        pdf_bytes = uploaded_pdf.read()

        try:
            reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            max_page_num = len(reader.pages)
        except Exception as e:
            st.error(f"Failed to process the PDF. Please ensure it is a valid file. Error: {e}")
            return

        # Permettre à l'utilisateur d'entrer plusieurs numéros de pages
        pages_input = st.text_input("Enter the page numbers to analyze (e.g., 1,3,5 or 2-4)", value="1")

        # Analyser l'entrée et générer une liste de pages
        pages = parse_pages_input(pages_input, max_page_num)

        if st.button("Analyze PDF") and pages:
            results = []
            total_pages = len(pages)
            for i, page_num in enumerate(pages, start=1):
                remaining_pages = total_pages - i
                estimated_time = remaining_pages * 30
                with st.spinner(
                        f'Analyzing page {page_num} of {max_page_num}. Remaining pages: {remaining_pages}. Estimated time left: {estimated_time} seconds'):
                    try:
                        # Convertir et analyser la page spécifique
                        pdf_image = convert_from_bytes(pdf_bytes, first_page=page_num, last_page=page_num)[0]
                        base64_image = encode_image_to_base64(pdf_image)
                        # Traitement hypothétique de l'image
                        data = asyncio.run(process_chat(base64_image, constants.SYST_PROMPT))
                        results.append(data)
                        # Mise à jour approximative pour chaque page traitée

                    except Exception as e:
                        st.error(f"Error processing page {page_num}: {e}")
                        continue

            # Afficher tous les résultats à la fin
            for result in results:
                show_tables(result)
        elif not pages:
            st.error("Invalid page numbers input. Please check your input and try again.")
    else:
        st.warning("Please upload a PDF.")


def parse_pages_input(pages_input, max_page_num):
    # Cette fonction devrait analyser la chaîne d'entrée et retourner une liste de numéros de pages
    # Par exemple, "1,3-5" devrait retourner [1, 3, 4, 5]
    # Implémentez cette logique selon vos besoins
    try:
        pages = []
        for part in pages_input.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.extend(range(start, min(end, max_page_num) + 1))
            else:
                page = int(part)
                if page <= max_page_num:
                    pages.append(page)
        return list(set(pages))  # Élimine les doublons et retourne la liste
    except Exception as e:
        st.error(f"Veillez a ne mettre uniquement des numeros de pages avec , et - ")

if __name__ == '__main__':
    display_data()
