import streamlit as st
from twilio.rest import Client
import os

ACCOUNT_SID = "account"
AUTH_TOKEN = "token"
TWILIO_PHONE = "*********"

# Streamlit UI
st.set_page_config(page_title="Twilio SMS Sender", page_icon="📱")
st.title("📲 Twilio SMS Sender")

st.markdown("""
Send SMS messages directly from your browser using Twilio and Python.""")


# User input
to_number = st.text_input("Recipient Phone Number (with country code)", "+91")
message_body = st.text_area("Your Message", "Hello from Python via Twilio! 🐍")

# Send button
if st.button("Send SMS"):
    if not to_number.strip() or not message_body.strip():
        st.warning("Please enter both the phone number and message.")
    else:
        try:
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            message = client.messages.create(
                body=message_body,
                from_=TWILIO_PHONE,
                to=to_number
            )
            st.success(f"✅ SMS sent successfully! Message SID: {message.sid}")
        except Exception as e:
            st.error(f"❌ Failed to send message: {e}")
