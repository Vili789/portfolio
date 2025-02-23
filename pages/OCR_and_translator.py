import streamlit as st
import os
import glob
import io
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
import pytesseract
from pdf2image import convert_from_path
from PIL import Image    
from fpdf import FPDF
from deep_translator import GoogleTranslator

st.title("PDF OCR & Translation")

# File uploader
uploaded_files = st.file_uploader("Upload PDF or Images", accept_multiple_files=True, type=["pdf", "png", "jpg"])

if uploaded_files:
    output_text = []
    
    for uploaded_file in uploaded_files:
        file_type = uploaded_file.type
        st.write(f"Processing `{uploaded_file.name}`...")

        # **Step 1: Save the uploaded file to a temporary location**
        temp_file_path = f"temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(uploaded_file.getbuffer())  # Save file to disk

        if file_type.startswith("image"):
            # **Step 2: Convert images to PDF**
            pdf = FPDF()
            pdf.add_page()
            img = Image.open(temp_file_path)
            pdf.image(temp_file_path, x=10, y=10, w=190)
            pdf_file_path = f"converted_{uploaded_file.name}.pdf"
            pdf.output(pdf_file_path, "F")
            file_path = pdf_file_path
        else:
            file_path = temp_file_path  # Use the saved PDF file

        # **Step 3: Convert PDF to images**
        try:
            images = convert_from_path(file_path)
            st.write(f"Converted `{uploaded_file.name}` into images successfully! ✅")
        except Exception as e:
            st.error(f"Error converting `{uploaded_file.name}` to images: {e}")
        
        # OCR processing
        pdf_writer = PdfWriter()
        for image in images:
            page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang='nld')
            pdf_page = PdfReader(io.BytesIO(page))
            pdf_writer.add_page(pdf_page.pages[0])
            text = pdf_page.pages[0].extract_text()
            output_text.append(text)

        # Save the processed PDF
        output_pdf_path = f"processed_{uploaded_file.name}"
        with open(output_pdf_path, 'wb') as f:
            pdf_writer.write(f)

        # Translate text
        words = text.lower().split()
        translated_words = [GoogleTranslator(source='nl', target='en').translate(word) for word in set(words)]
        translation_df = pd.DataFrame({"Original": list(set(words)), "Translated": translated_words})

        # Show results
        st.subheader("Extracted Text")
        st.text(text)
        st.subheader("Translations")
        st.dataframe(translation_df)
