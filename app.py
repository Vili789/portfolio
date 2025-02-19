import streamlit as st

st.set_page_config(page_title="My Portfolio", page_icon="👨‍💻", layout="wide")

st.title("👨‍💻 Welcome to My Portfolio")
st.write("Hello! I'm [Your Name], a software developer. Here are some of my projects:")

# Navigation links to main project pages
#st.page_link("pages/SeeWhoDoesntFollowYou/main.py", label="📊 Instagram Analyzer")
#st.page_link("pages/FlashcardAutomation/main.py", label="🤖 Flashcard Automation Tool")
#st.page_link("pages/Casino/main.py", label="🎰 Casino Game")

Casino = st.Page("Casino/main.py", title="Casino")
Insta = st.Page("SeeWhoDoesntFollowYou/main.py", title="Insta")
Flashcards = st.Page("FlashcardAutomation/main.py", title="Flashcards")

st.navigation(
    {
     "Casino": [Casino],
     "Insta": [Insta],
     "Flashcards": [Flashcards]
     }
    )
pg.run()
