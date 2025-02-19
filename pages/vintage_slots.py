import streamlit as st

st.set_page_config(page_title="Casino Game", page_icon="🎰")

with st.sidebar.expander("Welcome!"):
    st.page_link("app.py", label="Intorduction")
    
with st.sidebar.expander("📊 Instagram Analyzer"):
    st.page_link("pages/SeeWhoDoesntFollowYou.py", label="Home Page")

with st.sidebar.expander("🤖 Flashcard Automation Tool"):
    st.page_link("pages/FlashcardAutomation.py", label="Home Page")
    
with st.sidebar.expander("🎰 Casino"):
    st.page_link("pages/Casino.py", label="Home Page")
