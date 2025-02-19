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

st.markdown(
        """    
        🔍 **See Who Doesn't Follow You**  

        This tool allows you to **see the accounts that you follow but do not follow you back**.  
        If you have received the **Instagram ZIP file**, you can upload them here to:
        
        - 📌 See who **doesn't follow you back**.
        - 🔍 Find out **who you don’t follow back**.
        - 🤝 Identify **mutual followers**.
        """
    )
uploaded_file = st.file_uploader("Upload the Instagram Data ZIP file", type="zip")
if uploaded_file:
        try:
            with ZipFile(uploaded_file, 'r') as zip_file: 
                followers=zip_file.open('connections/followers_and_following/followers_1.json')
                followers = pd.read_json(followers)
                follower_link = []
                follower_username = []
                follower_followed_ts = []
                for i in range(len(followers)):
                    follower_link.append(followers['string_list_data'][i][0]['href'])
                    follower_username.append(followers['string_list_data'][i][0]['value'])
                    follower_followed_ts.append(followers['string_list_data'][i][0]['timestamp'])
                
                following=zip_file.open('connections/followers_and_following/following.json')
                following = pd.read_json(following)
                following_link = []
                following_username = []
                following_followed_ts = []
                for i in range(len(following)):
                    following_link.append(following['relationships_following'][i]['string_list_data'][0]['href'])
                    following_username.append(following['relationships_following'][i]['string_list_data'][0]['value'])
                    following_followed_ts.append(following['relationships_following'][i]['string_list_data'][0]['timestamp'])
                
                following_table = pd.DataFrame(
                    {'Username': following_username,
                     'Link': following_link,
                     'You Followed On': pd.to_datetime(following_followed_ts, unit='s')
                    })
                
                follower_table = pd.DataFrame(
                    {'Username': follower_username,
                     'Link': follower_link,
                     'Followed You On': pd.to_datetime(follower_followed_ts, unit='s')
                    })
                
                doesnt_follow_back = pd.merge(following_table, follower_table, on=['Username', 'Link'], how='left')
                doesnt_follow_back = doesnt_follow_back[doesnt_follow_back['Followed You On'].isnull()].reset_index(drop=True)
                
                you_dont_follow_back = pd.merge(following_table, follower_table, on=['Username', 'Link'], how='right')
                you_dont_follow_back = you_dont_follow_back[you_dont_follow_back['You Followed On'].isnull()].reset_index(drop=True)
                
                both_follow_eachother = pd.merge(following_table, follower_table, on=['Username', 'Link'], how='inner')

                st.subheader("Accounts That Do Not Follow You Back:")
                st.dataframe(doesnt_follow_back)

                st.subheader("Accounts That YOU Do Not Follow Back:")
                st.dataframe(you_dont_follow_back)

                st.subheader("Accounts That YOU Follow and They Follow You Back:")
                st.dataframe(both_follow_eachother)

        except Exception as e:
            st.error(f"Error reading file: {e}")
