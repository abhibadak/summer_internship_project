import streamlit as st
import pywhatkit as kit
import datetime
import re

# Page configuration
st.set_page_config(page_title="WhatsApp Message Sender", page_icon="📱", layout="centered")

# App title
st.title("📱 WhatsApp Message Sender")
st.write("Quickly send or schedule WhatsApp messages from your browser.")

# Sidebar help
with st.sidebar:
    st.header("How it works:")
    st.markdown("""
    - ✅ Make sure WhatsApp Web is open in your browser  
    - 📲 Use full phone number with country code (e.g., `+91XXXXXXXXXX`)  
    - ✏️ Type a short message like a human would  
    - 🕒 You can send it now or schedule it  
    """)

# Phone number validator
def is_valid_number(phone):
    return re.match(r"^\+\d{10,15}$", phone)

tab1, tab2 = st.tabs(["📤 Send Now", "⏰ Schedule"])

# ---------------------- Send Now ----------------------
with tab1:
    st.subheader("Send Message Instantly")
    phone = st.text_input("Phone Number", value="+91", key="phone_now")
    message = st.text_area("Your Message", placeholder="Hi! Just wanted to say hello 👋", key="msg_now")

    if st.button("Send Now"):
        if not is_valid_number(phone) or not message.strip():
            st.warning("Please enter a valid number and a short message.")
        else:
            try:
                st.info("Opening WhatsApp Web... please wait a few seconds.")
                kit.sendwhatmsg_instantly(
                    phone_no=phone,
                    message=message,
                    wait_time=10,
                    tab_close=True
                )
                st.success("✅ Message sent! Check your WhatsApp.")
            except Exception as e:
                st.error("Something went wrong.")
                st.text(str(e))

# ---------------------- Schedule ----------------------
with tab2:
    st.subheader("Schedule Message")
    phone_sched = st.text_input("Phone Number", value="+91", key="phone_sched")
    message_sched = st.text_area("Your Message", placeholder="Hey! Just checking in 🤝", key="msg_sched")

    col1, col2 = st.columns(2)
    with col1:
        hour = st.number_input("Hour (24h format)", 0, 23, value=datetime.datetime.now().hour)
    with col2:
        minute = st.number_input("Minute", 0, 59, value=(datetime.datetime.now().minute + 2) % 60)

    if st.button("Schedule"):
        if not is_valid_number(phone_sched) or not message_sched.strip():
            st.warning("Enter a valid number and message.")
        else:
            now = datetime.datetime.now()
            send_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if send_time <= now:
                st.error("Please select a future time.")
            else:
                try:
                    st.info(f"Scheduling message for {hour:02d}:{minute:02d}...")
                    kit.sendwhatmsg(
                        phone_no=phone_sched,
                        message=message_sched,
                        time_hour=hour,
                        time_min=minute,
                        wait_time=10,
                        tab_close=True
                    )
                    st.success("✅ Message scheduled. Don’t close your browser until it’s sent.")
                except Exception as e:
                    st.error("Couldn’t schedule the message.")
                    st.text(str(e))

# Footer note
st.markdown("---")
st.caption("🔒 Your messages are sent directly through your own WhatsApp. Nothing is stored or shared.")
