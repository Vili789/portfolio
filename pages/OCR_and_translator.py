import streamlit as st
import os
import glob
import requests
import io
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
import pytesseract
from pdf2image import convert_from_path
from PIL import Image    
from fpdf import FPDF
from deep_translator import GoogleTranslator

st.title("PDF OCR & Translation")

# ✅ **Create a Local Tesseract Language Directory**
TESSDATA_DIR = os.path.abspath("tessdata")  # Use a local directory
os.makedirs(TESSDATA_DIR, exist_ok=True)
os.environ["TESSDATA_PREFIX"] = TESSDATA_DIR  # Set environment variable

# ✅ **Define Languages to Install**
languages = ["eng", "nld", "deu", "fra", "spa", "ita", "por", "rus", "ara", "chi_sim"]
installed_languages = [f.split(".")[0] for f in os.listdir(TESSDATA_DIR) if f.endswith(".traineddata")]

# ✅ **Download Missing Language Files**
tessdata_repo = "https://github.com/tesseract-ocr/tessdata/raw/main/"
for lang in languages:
    lang_file = os.path.join(TESSDATA_DIR, f"{lang}.traineddata")
    if lang not in installed_languages:
        st.write(f"🔄 Downloading `{lang}.traineddata`...")
        url = tessdata_repo + f"{lang}.traineddata"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(lang_file, "wb") as f:
                f.write(response.content)
            st.write(f"✅ `{lang}.traineddata` installed!")
        else:
            st.warning(f"❌ Failed to download `{lang}.traineddata`.")

# ✅ **Refresh installed languages**
installed_languages = [f.split(".")[0] for f in os.listdir(TESSDATA_DIR) if f.endswith(".traineddata")]
st.write(f"📌 Installed Tesseract Languages: `{', '.join(installed_languages)}`")

# ✅ **Set Tesseract Binary Path**
if os.path.exists("/usr/bin/tesseract"):  # Cloud/Linux
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
    
# 📤 File Uploader
uploaded_files = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg"])

# 📌 Language selection dropdown
language_choice = st.selectbox("Select OCR Language", installed_languages, index=0)

if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file is None:
            st.error("No file uploaded. Please select a file.")
            continue

        # ✅ **Fix for 'bytes' object error**
        try:
            file_name = uploaded_file.name  # Works when file is an object
        except AttributeError:
            file_name = "uploaded_file.pdf"  # Assign a default name if file is bytes

        st.write(f"Processing `{file_name}` using `{language_choice}` OCR...")

        # ✅ **Step 1: Save the uploaded file to a temporary location**
        temp_file_path = f"temp_{file_name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # ✅ **Step 2: Convert PDF to images (if applicable)**
        if file_name.endswith(".pdf"):
            images = convert_from_path(temp_file_path)
        else:
            images = [Image.open(temp_file_path)]

        # ✅ **Step 3: Run OCR on images**
        extracted_text = ""
        for image in images:
            text = pytesseract.image_to_string(image, lang=language_choice)
            extracted_text += text + "\n"
        
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
