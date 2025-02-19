import streamlit as st

st.set_page_config(page_title="My Portfolio", page_icon="👨‍💻", layout="wide")

st.title("👨‍💻 Welcome to My Portfolio")
st.write("Hello! I'm [Your Name], a software developer. Here are some of my projects:")

# Correcting the file paths
st.page_link("pages/SeeWhoDoesntFollowYou.py", label="📊 Instagram Analyzer", in_navigation=False)
st.page_link("pages/FlashcardAutomation.py", label="🤖 Flashcard Automation Tool", in_navigation=False)
st.page_link("pages/Casino.py", label="🎰 Casino Game", in_navigation=False)

with st.sidebar.expander("📊 Instagram Analyzer"):
    st.page_link("pages/SeeWhoDoesntFollowYou.py", label="Home Page")

with st.sidebar.expander("🤖 Flashcard Automation Tool"):
    st.page_link("pages/FlashcardAutomation.py", label="Home Page")
    
with st.sidebar.expander("🎰 Casino"):
    st.page_link("pages/Casino.py", label="Home Page")

