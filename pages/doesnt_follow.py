import streamlit as st

st.set_page_config(page_title="See Who Doesn't Follow You Back")#, page_icon="📊")

with st.sidebar.expander("📊 Instagram Analyzer"):
    st.page_link("pages/SeeWhoDoesntFollowYou.py", label="Home Page")
    st.page_link("pages/doesnt_follow.py", label="See Who Doesn't Follow You Back")
    st.page_link("pages/compare_changes.py", label="Compare Changes Over Time")

with st.sidebar.expander("🤖 Flashcard Automation Tool"):
    st.page_link("pages/FlashcardAutomation.py", label="Home Page")
    
with st.sidebar.expander("🎰 Casino"):
    st.page_link("pages/Casino.py", label="Home Page")
