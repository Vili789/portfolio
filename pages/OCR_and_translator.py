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

# ✅ **Define Tesseract data directory**
TESSDATA_DIR = "/usr/share/tesseract-ocr/4.00/tessdata/"
os.environ["TESSDATA_PREFIX"] = TESSDATA_DIR  # Set environment variable

# ✅ **Check available languages**
installed_languages = os.listdir(TESSDATA_DIR) if os.path.exists(TESSDATA_DIR) else []
st.write(f"📌 Installed Tesseract Languages: `{', '.join(installed_languages)}`")

# ✅ **Auto-download ALL Tesseract languages if missing**
if not installed_languages:
    st.write("🔄 Downloading full Tesseract language dataset... (This may take a while)")

    tessdata_repo = "https://github.com/tesseract-ocr/tessdata/raw/main/"
    languages = ["eng", "nld", "deu", "fra", "spa", "ita", "por", "rus", "ara", "chi_sim"]  # Add more as needed

    os.makedirs(TESSDATA_DIR, exist_ok=True)

    for lang in languages:
        lang_path = os.path.join(TESSDATA_DIR, f"{lang}.traineddata")
        if not os.path.exists(lang_path):
            url = tessdata_repo + f"{lang}.traineddata"
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(lang_path, "wb") as f:
                    f.write(response.content)
                st.write(f"✅ Installed `{lang}` language for Tesseract.")
            else:
                st.warning(f"❌ Failed to download `{lang}.traineddata`")

    # Refresh installed languages list
    installed_languages = os.listdir(TESSDATA_DIR)
    st.write(f"🎉 Installed Languages: `{', '.join(installed_languages)}`")

# ✅ **Set Tesseract binary path (For Streamlit Cloud)**
if os.path.exists("/usr/bin/tesseract"):  # Cloud/Linux
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
else:  # Windows (Local)
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# 📤 File Uploader
uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg"])

# 📌 Language selection dropdown
language_choice = st.selectbox("Select OCR Language", installed_languages, index=0)

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
