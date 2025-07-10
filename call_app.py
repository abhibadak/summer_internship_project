import streamlit as st
from twilio.rest import Client
import os
import requests

# --- Twilio Credentials (Replace with your own or load securely) ---
ACCOUNT_SID = "ACb3e5f3dc7f2de4a91ead8b0c0974b565"
AUTH_TOKEN = "ee586b707d104595d9bcbc62a67aca89"
TWILIO_PHONE = "+15074185310"  # Your Twilio number

# --- Streamlit UI ---
st.set_page_config(page_title="📞 Twilio Call Sender", page_icon="📱", layout="centered")
st.title("📞 Twilio Voice Caller")
st.markdown("Send a real voice call using Twilio + Python.")

# Inputs
to_number = st.text_input("Recipient Phone Number", "+91XXXXXXXXXX")
voice_message = st.text_area("What do you want the call to say?", "Hello! This is a test call using Python.")

# Call button
if st.button("📞 Call Now"):
    if not to_number.strip() or not voice_message.strip():
        st.warning("Please enter both phone number and message.")
    else:
        # Dynamically generate TwiML
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice">{voice_message}</Say>
</Response>"""

        # Host TwiML temporarily using httpbin or use your own server
        # For testing: use Pastebin, Replit, GitHub raw, or static site
        # For now, simulate using a known Twilio demo TwiML
        # Use this only if you don't have your own URL:
        fallback_twiml_url = "http://demo.twilio.com/docs/voice.xml"

        try:
            client = Client(ACCOUNT_SID, AUTH_TOKEN)

            call = client.calls.create(
                to=to_number,
                from_=TWILIO_PHONE,
                url=fallback_twiml_url  # Replace with your hosted TwiML XML URL for custom messages
            )

            st.success(f"✅ Call initiated! Call SID: {call.sid}")
        except Exception as e:
            st.error(f"❌ Failed to initiate call: {e}")
