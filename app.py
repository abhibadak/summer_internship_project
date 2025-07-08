import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from twilio.rest import Client
import tweepy
import time

# Page configuration
st.set_page_config(page_title="Multi-Platform Messenger", layout="wide")

# Sidebar for credentials
with st.sidebar:
    st.title("Credentials Configuration")
    
    # Twilio Credentials
    st.subheader("Twilio (SMS/Calls)")
    twilio_account_sid = st.text_input("Twilio Account SID")
    twilio_auth_token = st.text_input("Twilio Auth Token", type="password")
    twilio_phone_number = st.text_input("Twilio Phone Number")
    
    # Email Credentials
    st.subheader("Email Settings")
    email_address = st.text_input("Your Email Address")
    email_password = st.text_input("Email Password", type="password")
    smtp_server = st.text_input("SMTP Server", "smtp.gmail.com")
    smtp_port = st.number_input("SMTP Port", 587)
    
    # Twitter API
    st.subheader("Twitter API")
    twitter_api_key = st.text_input("Twitter API Key")
    twitter_api_secret = st.text_input("Twitter API Secret", type="password")
    twitter_access_token = st.text_input("Twitter Access Token")
    twitter_access_secret = st.text_input("Twitter Access Secret", type="password")
    
    # LinkedIn API
    st.subheader("LinkedIn API")
    linkedin_access_token = st.text_input("LinkedIn Access Token", type="password")

# Main App
st.title("Multi-Platform Messenger")

# Tab interface
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "WhatsApp", "Instagram", "Email", 
    "SMS", "Phone Call", "LinkedIn", "Twitter"
])

# WhatsApp Tab
with tab1:
    st.header("Send WhatsApp Message")
    whatsapp_number = st.text_input("Recipient WhatsApp Number (with country code)", key="whatsapp_num")
    whatsapp_message = st.text_area("WhatsApp Message", key="whatsapp_msg")
    
    if st.button("Send WhatsApp Message"):
        if not all([twilio_account_sid, twilio_auth_token, whatsapp_number, whatsapp_message]):
            st.error("Please fill all required fields and configure Twilio credentials")
        else:
            try:
                client = Client(twilio_account_sid, twilio_auth_token)
                message = client.messages.create(
                    body=whatsapp_message,
                    from_='whatsapp:' + twilio_phone_number,
                    to='whatsapp:' + whatsapp_number
                )
                st.success(f"Message sent! SID: {message.sid}")
            except Exception as e:
                st.error(f"Error sending WhatsApp message: {str(e)}")

# Instagram Tab
with tab2:
    st.header("Send Instagram Message")
    st.warning("Instagram API access is limited. This might require a third-party service.")
    instagram_username = st.text_input("Recipient Instagram Username")
    instagram_message = st.text_area("Instagram Message")
    
    if st.button("Send Instagram Message"):
        st.info("Instagram integration would require a third-party service or official API access")

# Email Tab
with tab3:
    st.header("Send Email")
    recipient_email = st.text_input("Recipient Email Address")
    email_subject = st.text_input("Email Subject")
    email_body = st.text_area("Email Body")
    
    if st.button("Send Email"):
        if not all([email_address, email_password, recipient_email, email_subject]):
            st.error("Please fill all required fields and configure email credentials")
        else:
            try:
                msg = MIMEMultipart()
                msg['From'] = email_address
                msg['To'] = recipient_email
                msg['Subject'] = email_subject
                msg.attach(MIMEText(email_body, 'plain'))
                
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(email_address, email_password)
                server.sendmail(email_address, recipient_email, msg.as_string())
                server.quit()
                
                st.success("Email sent successfully!")
            except Exception as e:
                st.error(f"Error sending email: {str(e)}")

# SMS Tab
with tab4:
    st.header("Send SMS")
    sms_number = st.text_input("Recipient Phone Number (with country code)", key="sms_num")
    sms_message = st.text_area("SMS Message", key="sms_msg")
    
    if st.button("Send SMS"):
        if not all([twilio_account_sid, twilio_auth_token, sms_number, sms_message]):
            st.error("Please fill all required fields and configure Twilio credentials")
        else:
            try:
                client = Client(twilio_account_sid, twilio_auth_token)
                message = client.messages.create(
                    body=sms_message,
                    from_=twilio_phone_number,
                    to=sms_number
                )
                st.success(f"SMS sent! SID: {message.sid}")
            except Exception as e:
                st.error(f"Error sending SMS: {str(e)}")

# Phone Call Tab
with tab5:
    st.header("Make Phone Call")
    call_number = st.text_input("Recipient Phone Number (with country code)", key="call_num")
    call_message = st.text_area("Message to speak", key="call_msg")
    
    if st.button("Make Call"):
        if not all([twilio_account_sid, twilio_auth_token, call_number, call_message]):
            st.error("Please fill all required fields and configure Twilio credentials")
        else:
            try:
                client = Client(twilio_account_sid, twilio_auth_token)
                call = client.calls.create(
                    twiml=f'<Response><Say>{call_message}</Say></Response>',
                    from_=twilio_phone_number,
                    to=call_number
                )
                st.success(f"Call initiated! SID: {call.sid}")
            except Exception as e:
                st.error(f"Error making call: {str(e)}")

# LinkedIn Tab
with tab6:
    st.header("Create LinkedIn Post")
    linkedin_post = st.text_area("Post Content")
    post_visibility = st.selectbox("Post Visibility", ["PUBLIC", "CONNECTIONS"])
    
    if st.button("Post to LinkedIn"):
        if not linkedin_access_token:
            st.error("Please configure LinkedIn Access Token")
        else:
            try:
                # This is a simplified example - LinkedIn API is more complex
                headers = {
                    'Authorization': f'Bearer {linkedin_access_token}',
                    'Content-Type': 'application/json',
                }
                
                post_data = {
                    "author": "urn:li:person:YOUR_USER_ID",  # You'd need to get this
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
                    st.success("Post created successfully!")
                else:
                    st.error(f"Error creating post: {response.text}")
            except Exception as e:
                st.error(f"Error posting to LinkedIn: {str(e)}")

# Twitter Tab
with tab7:
    st.header("Post to Twitter")
    tweet_content = st.text_area("Tweet Content")
    
    if st.button("Post Tweet"):
        if not all([twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_secret]):
            st.error("Please configure Twitter API credentials")
        else:
            try:
                auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
                auth.set_access_token(twitter_access_token, twitter_access_secret)
                api = tweepy.API(auth)
                
                # Verify credentials
                api.verify_credentials()
                api.update_status(tweet_content)
                st.success("Tweet posted successfully!")
            except Exception as e:
                st.error(f"Error posting tweet: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Note: Some features require paid services like Twilio or API access to platforms.")