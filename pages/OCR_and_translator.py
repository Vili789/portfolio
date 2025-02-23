import streamlit as st
import os
import glob
import requests
import tempfile 
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
    
# File uploader
uploaded_files = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg"], accept_multiple_files=True)

for uploaded_file in uploaded_files:
    st.write("Filename:", uploaded_file.name)

    # Handle PDFs
    if uploaded_file.type == "application/pdf":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name  # Get the temporary file path

        # Convert PDF to images
        images = convert_from_path(temp_file_path)

        # Display images
        for img in images:
            st.image(img, caption="Page Preview", use_column_width=True)

        # Clean up temporary file
        os.remove(temp_file_path)

    # Handle Images
    elif uploaded_file.type in ["image/png", "image/jpeg"]:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)
