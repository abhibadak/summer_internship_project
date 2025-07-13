import streamlit as st
import requests

st.set_page_config(page_title="Social Media Poster", layout="centered")

st.title("📣 Social Media Poster")

# ------------------ Sidebar Config ------------------ #
st.sidebar.header("🔐 API Configuration")

# LinkedIn
linkedin_access_token = st.sidebar.text_input("LinkedIn Access Token", type="password")
linkedin_user_id = st.sidebar.text_input("LinkedIn User ID (URN format: urn:li:person:xxxxxx)")

# ------------------ Tabs ------------------ #
tab1, = st.tabs(["📌 LinkedIn"])  # Fix here

# ------------------ LinkedIn Tab ------------------ #
with tab1:
    st.header("Create LinkedIn Post")
    linkedin_post = st.text_area("Post Content")
    post_visibility = st.selectbox("Post Visibility", ["PUBLIC", "CONNECTIONS"])

    if st.button("Post to LinkedIn"):
        if not linkedin_access_token or not linkedin_user_id:
            st.error("Please provide LinkedIn Access Token and User ID.")
        else:
            try:
                headers = {
                    'Authorization': f'Bearer {linkedin_access_token}',
                    'Content-Type': 'application/json',
                    'X-Restli-Protocol-Version': '2.0.0'
                }

                post_data = {
                    "author": linkedin_user_id,
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {
                                "text": linkedin_post
                            },
                            "shareMediaCategory": "NONE"
                        }
                    },
                    "visibility": {
                        "com.linkedin.ugc.MemberNetworkVisibility": post_visibility
                    }
                }

                response = requests.post(
                    'https://api.linkedin.com/v2/ugcPosts',
                    headers=headers,
                    json=post_data
                )

                if response.status_code == 201:
                    st.success("✅ LinkedIn post created successfully!")
                else:
                    st.error(f"❌ Failed to post to LinkedIn: {response.text}")
            except Exception as e:
                st.error(f"🔴 Exception: {str(e)}")
