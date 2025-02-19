import streamlit as st

st.set_page_config(page_title="My Portfolio", page_icon="👨‍💻", layout="wide")

st.title("👨‍💻 Welcome to My Portfolio")
st.write("Hello! I'm [Your Name], a software developer. Here are some of my projects:")

# Correcting the file paths
st.page_link("pages/SeeWhoDoesntFollowYou.py", label="📊 Instagram Analyzer")
st.page_link("pages/FlashcardAutomation.py", label="🤖 Flashcard Automation Tool")
st.page_link("pages/Casino.py", label="🎰 Casino Game")
