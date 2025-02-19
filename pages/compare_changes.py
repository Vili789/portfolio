import streamlit as st
import pandas as pd
from zipfile import ZipFile
from datetime import datetime

st.set_page_config(page_title="Compare Changes Over Time")#, page_icon="📊")

with st.sidebar.expander("📊 Instagram Analyzer"):
    st.page_link("pages/SeeWhoDoesntFollowYou.py", label="Home Page")
    st.page_link("pages/doesnt_follow.py", label="See Who Doesn't Follow You Back")
    st.page_link("pages/compare_changes.py", label="Compare Changes Over Time")

with st.sidebar.expander("🤖 Flashcard Automation Tool"):
    st.page_link("pages/FlashcardAutomation.py", label="Home Page")
    
with st.sidebar.expander("🎰 Casino"):
    st.page_link("pages/Casino.py", label="Home Page")

st.write(
    """
    🔍 **Compare Changes Over Time**  

    This tool allows you to **track changes in your Instagram followers and following lists** over time.  
    If you have saved **older Instagram ZIP files**, you can upload them here along with a **newer ZIP file** to:
    
    - 🆕 Identify **new followers** you've gained.
    - 🚶‍♂️ Find out **who unfollowed you**.
    - ➕ See **who you started following**.
    - ➖ Check **who you unfollowed**.

    ---
    
    ⚠ **Important:**  
    - This **only works if you have previously saved ZIP files** from past downloads.  
    - I **highly recommend** creating a **dedicated folder on your computer** to store all your Instagram ZIP files **whenever you download them**.  
    - **Do NOT unzip the files**—upload them as they are.  

    ---
    
    📝 **P.S.**  
    If you download **both the old and new files on the same day**, Instagram will **timestamp them with the download date, not the request date**.  
    This means you might not see accurate comparisons if you download multiple files in one session. You could, however, manually change the name of the file to reflect the actual day of data retrieval, in which case this would not be an issue. Nevertheless, it is still recommended to keep your older files as Instagram only allows downloading them for 7 days after requesting them.
            
    ---
    """
)

    
uploaded_file1 = st.file_uploader("Upload the OLDER Instagram Data ZIP file here", type="zip")
uploaded_file2 = st.file_uploader("Upload the NEWER Instagram Data ZIP file here", type="zip")
    
if uploaded_file1 and uploaded_file2:
        try:
            with ZipFile(uploaded_file1, 'r') as zip_file:                 
                old_followers=zip_file.open('connections/followers_and_following/followers_1.json')
                old_followers = pd.read_json(old_followers)
                old_follower_link = []
                old_follower_username = []
                old_follower_followed_ts = []
                for i in range(len(old_followers)):
                    old_follower_link.append(old_followers['string_list_data'][i][0]['href'])
                    old_follower_username.append(old_followers['string_list_data'][i][0]['value'])
                    old_follower_followed_ts.append(old_followers['string_list_data'][i][0]['timestamp'])
                
                old_following=zip_file.open('connections/followers_and_following/following.json')
                old_following = pd.read_json(old_following)
                old_following_link = []
                old_following_username = []
                old_following_followed_ts = []
                for i in range(len(old_following)):
                    old_following_link.append(old_following['relationships_following'][i]['string_list_data'][0]['href'])
                    old_following_username.append(old_following['relationships_following'][i]['string_list_data'][0]['value'])
                    old_following_followed_ts.append(old_following['relationships_following'][i]['string_list_data'][0]['timestamp'])
                
                old_following_table = pd.DataFrame(
                    {'Username': old_following_username,
                     'Link': old_following_link,
                     'You Followed On (old)': pd.to_datetime(old_following_followed_ts, unit='s')
                    })
                
                old_follower_table = pd.DataFrame(
                    {'Username': old_follower_username,
                     'Link': old_follower_link,
                     'Followed You On (old)': pd.to_datetime(old_follower_followed_ts, unit='s')
                    })
                
            with ZipFile(uploaded_file2, 'r') as zip_file:                 
                new_followers=zip_file.open('connections/followers_and_following/followers_1.json')
                new_followers = pd.read_json(new_followers)
                new_follower_link = []
                new_follower_username = []
                new_follower_followed_ts = []
                for i in range(len(new_followers)):
                    new_follower_link.append(new_followers['string_list_data'][i][0]['href'])
                    new_follower_username.append(new_followers['string_list_data'][i][0]['value'])
                    new_follower_followed_ts.append(new_followers['string_list_data'][i][0]['timestamp'])
                
                new_following=zip_file.open('connections/followers_and_following/following.json')
                new_following = pd.read_json(new_following)
                new_following_link = []
                new_following_username = []
                new_following_followed_ts = []
                for i in range(len(new_following)):
                    new_following_link.append(new_following['relationships_following'][i]['string_list_data'][0]['href'])
                    new_following_username.append(new_following['relationships_following'][i]['string_list_data'][0]['value'])
                    new_following_followed_ts.append(new_following['relationships_following'][i]['string_list_data'][0]['timestamp'])
                
                new_following_table = pd.DataFrame(
                    {'Username': new_following_username,
                     'Link': new_following_link,
                     'You Followed On (new)': pd.to_datetime(new_following_followed_ts, unit='s')
                    })
                
                new_follower_table = pd.DataFrame(
                    {'Username': new_follower_username,
                     'Link': new_follower_link,
                     'Followed You On (new)': pd.to_datetime(new_follower_followed_ts, unit='s')
                    })

            follower_change_table = pd.merge(new_follower_table, old_follower_table, on=['Username', 'Link'], how='outer')
            gained_followers = follower_change_table[follower_change_table['Followed You On (old)'].isnull()]
            lost_followers = follower_change_table[follower_change_table['Followed You On (new)'].isnull()]

            following_change_table = pd.merge(new_following_table, old_following_table, on=['Username', 'Link'], how='outer')
            you_followed = following_change_table[following_change_table['You Followed On (old)'].isnull()].reset_index()
            you_unfollowed = following_change_table[following_change_table['You Followed On (new)'].isnull()].reset_index()
            
            file_timestamp_older = datetime(int(uploaded_file1.name.split('-')[2]), int(uploaded_file1.name.split('-')[3]), int(uploaded_file1.name.split('-')[4]))
            file_timestamp_newer = datetime(int(uploaded_file2.name.split('-')[2]), int(uploaded_file2.name.split('-')[3]), int(uploaded_file2.name.split('-')[4]))
            
            # Format the dates (DD-MM-YYYY)
            older_date = file_timestamp_older.strftime("%d-%m-%Y")
            newer_date = file_timestamp_newer.strftime("%d-%m-%Y")

            st.subheader(f"Followers you gained between {older_date} and {newer_date}:")
            st.dataframe(gained_followers)

            st.subheader(f"Followers you lost between {older_date} and {newer_date}:")
            st.dataframe(lost_followers)

            st.subheader(f"Accounts you followed between {older_date} and {newer_date}:")
            st.dataframe(you_followed)

            st.subheader(f"Accounts you unfollowed between {older_date} and {newer_date}:")
            st.dataframe(you_unfollowed)
            
        except Exception as e:
            st.error(f"Error reading file: {e}")

st.page_link("pages/doesnt_follow.py", label="See Who Doesn't Follow You")
st.page_link("pages/SeeWhoDoesntFollowYou.py", label="Go Back")
