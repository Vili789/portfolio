import streamlit as st

st.set_page_config(page_title="Instagram Analyzer", page_icon="📊")

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

st.markdown(
        """
        # 📊 Instagram Follower Analyzer  
        **Find out who follows you back and who doesn’t!**  

        Welcome to the **Instagram Follower Analyzer**, a simple tool that helps you:
        
        See Who Doesn't Follow You
        - 📌 See who **doesn't follow you back**.
        - 🔍 Find out **who you don’t follow back**.
        - 🤝 Identify **mutual followers**.

        Compare Changes Over Time
        - 🆕 Identify **new followers** you've gained.
        - 🚶‍♂️ Find out **who unfollowed you**.
        - ➕ See **who you started following**.
        - ➖ Check **who you unfollowed**.
        ---
        ## 📥 **How to Get Your Instagram Data ZIP File**
        To use this tool, you need to **download your Instagram data**.  
        Follow these steps **carefully**:  

        1️⃣ **Go to Instagram Activity**  
            - Phone: Open Instagram, go on your profile and click on the ☰ three-line menu icon in the top right corner.  
            - Web browser: Open Instagram and click on the ☰ three-line menu icon in the bottom left corner  → Click **"Your Activity"**.
          
        2️⃣ **Find Your Information**  
            - On your phone, scroll to **"How You Use Instagram"** → Click **"Your Activity"**.  If you're using a browser this will open a new page.
            - Scroll **all the way down** to **"Download Your Information"**.  
            - Click **"Download or Transfer Information"**.  
            - Select your account.  
            - Choose **"Some of your information"**.  
            - Under **"Connections"**, tick the box for **Followers and Following**.  
            - Click **Next** → **Download to Device**.

        3️⃣ **Request the Data in the Right Format**    
            - Choose **Date Range: All Time**.  
            - **Format: JSON** (**not HTML!**).  
            - Click **Create files**.

        4️⃣ **Upload the ZIP File Here**  
            - Instagram will send you a **ZIP file** with your data.  
            - **Do NOT unzip it** – upload the ZIP file directly here.  

        📌 **Once uploaded, the app will analyze your followers and following!** 🎉  
        
        ###### PS: If you click on another page in the navigation panel you will have to re-upload your zip file!     
        ---
        ## 🔒 **Privacy First: Your Data Stays with You!**  
        This app **does not store, process, or send** your data anywhere.  
        - The file you upload **stays on your device**.  
        - Your **privacy is 100% secure**.  
        - **Streamlit does not store** any files you upload. 
        
        ---
        
        ## 📊 Ready to analyze? Choose a tool from the sidebar or from below! 🚀 
        """
    )

st.page_link("pages/doesnt_follow.py", label="See Who Doesn't Follow You")
st.page_link("pages/compare_changes.py", label="Compare Changes Over Time")
st.page_link("app.py", label="Go Back")

