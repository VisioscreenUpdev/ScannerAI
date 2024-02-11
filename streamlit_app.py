import aiFunctions as ai
import itertools
import pandas as pd
import PyPDF2
import asyncio
import streamlit as st
import base64
from pdf2image import convert_from_bytes
import io



def show_tables(json_data):
    two_price_field = "Prix UNITE 2"
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


def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def AnalyzeSelectedPages(pages,max_page_num,pdf_bytes):
    results = []
    total_pages = len(pages)
    for i, page_num in enumerate(pages, start=1):
        remaining_pages = total_pages - i
        estimated_time = 30 + remaining_pages * 30
        with st.spinner(
                f'Analyse IA de la page {page_num} . {remaining_pages} pages restantes . Temps estimé avant la fin : {estimated_time} secondes.'):
            try:
                pdf_image = convert_from_bytes(pdf_bytes, first_page=page_num, last_page=page_num)[0]
                base64_image = encode_image_to_base64(pdf_image)
                data = asyncio.run(ai.scan_image(base64_image))
                results.append(data)

            except Exception as e:
                st.error(f"Une erreur s'est produite lors du traitement de la page {page_num}. Veuillez réessayer ultérieurement.")
                continue
    return list(itertools.chain.from_iterable(results))


def display_data():
    st.title("IA Scanner by VisioScreen")
    uploaded_pdf = st.file_uploader("Veuillez importer un PDF", type=["pdf"])
    if uploaded_pdf:
        pdf_bytes = uploaded_pdf.read()
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            max_page_num = len(reader.pages)
        except Exception as e:
            st.error("La tentative de traitement du PDF a échoué. Veuillez vérifier que le fichier est valide.")
            print(f"La tentative de traitement du PDF a échoué. Veuillez vérifier que le fichier est valide. Détail de l'erreur : {e}")
            return
        pages_input = st.text_input("Entrez les numéros des pages à analyser (par exemple, 1,3,5 ou 2-4)", value="1")
        pages = parse_pages_input(pages_input, max_page_num)

        if st.button("Analyze PDF") and pages:
            result = AnalyzeSelectedPages(pages,max_page_num,pdf_bytes)
            show_tables(result)


def parse_pages_input(pages_input, max_page_num):
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
                else:
                    st.error(f"Une ou plusieurs pages ne sont pas dans l'intervalle du catalogue 1-{max_page_num}")
                    return
        return list(set(pages))
    except Exception as e:
        st.error("Veuillez uniquement utiliser des numéros de pages, séparés par des virgules (,) et des tirets (-)")

if __name__ == '__main__':
    display_data()
