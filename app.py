import streamlit as st

st.set_page_config(page_title="My Portfolio", page_icon="👨‍💻", layout="wide")

st.title("👨‍💻 Welcome to My Portfolio")
st.write("Hello! My name is Vilmos Kutnyanszky, and I'm expanding my Python skills by developing fun and random projects for anyone to use. Here are some of my projects:")

# Correcting the file paths
st.page_link("pages/SeeWhoDoesntFollowYou.py", label="📊 Instagram Analyzer")
st.page_link("pages/FlashcardAutomation.py", label="🤖 Flashcard Automation Tool")
st.page_link("pages/Casino.py", label="🎰 Casino Game")

with st.sidebar.expander("Welcome!"):
    st.page_link("app.py", label="Intorduction")
    
with st.sidebar.expander("📊 Instagram Analyzer"):
    st.page_link("pages/SeeWhoDoesntFollowYou.py", label="Home Page")
    st.page_link("pages/doesnt_follow.py", label="See Who Doesn't Follow You Back")
    st.page_link("pages/compare_changes.py", label="Compare Changes Over Time")

with st.sidebar.expander("🤖 Flashcard Automation Tool"):
    st.page_link("pages/FlashcardAutomation.py", label="Home Page")
    
with st.sidebar.expander("🎰 Casino"):
    st.page_link("pages/Casino.py", label="Home Page")

