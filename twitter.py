import streamlit as st
import tweepy

#Twitter API Credentials
twitter_api_key = "xxyyxx"
twitter_api_secret = "xxyyxx"
twitter_access_token = "xxyyxx"
twitter_access_secret = "xxyyyxx"

#Streamlit UI ---
st.header("Post to Twitter")
tweet_content = st.text_area("Tweet Content", max_chars=280)

if st.button("Post Tweet"):
    if not tweet_content.strip():
        st.warning("Tweet content cannot be empty.")
    else:
        try:
            # Authenticate
            auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
            auth.set_access_token(twitter_access_token, twitter_access_secret)
            api = tweepy.API(auth)

            # Post tweet
            api.verify_credentials()
            api.update_status(tweet_content)
            st.success("✅ Tweet posted successfully!")

        except tweepy.errors.TweepyException as e:
            st.error(f"Twitter error: {str(e)}")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
