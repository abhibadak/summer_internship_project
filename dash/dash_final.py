# Save this entire code as your app.py file

import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from urllib.parse import urlparse
import os
import datetime
import re
import sys
from PIL import Image, ImageDraw, ImageFont
import io
import time
import streamlit.components.v1 as components

# --- Load environment variables ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    st.warning("`python-dotenv` not found. Ensure environment variables are set in your deployment environment.")

# --- Conditional imports for all APIs ---
try:
    from twilio.rest import Client
except ImportError:
    Client = None
try:
    import pywhatkit as kit
except ImportError:
    kit = None
try:
    import tweepy
except ImportError:
    tweepy = None
try:
    import boto3
    from botocore.exceptions import ClientError, WaiterError
except ImportError:
    boto3 = None
try:
    import google.generativeai as genai
except ImportError:
    genai = None
try:
    import paramiko
except ImportError:
    paramiko = None
try:
    from instagrapi import Client as InstaClient
except ImportError:
    InstaClient = None
try:
    import cv2
    import mediapipe as mp
    from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
except ImportError:
    cv2, mp, VideoTransformerBase, webrtc_streamer = None, None, object, None
try:
    import psutil
except ImportError:
    psutil = None
try:
    import docker
except ImportError:
    docker = None
try:
    import shutil
except ImportError:
    shutil = None


# --- Configuration Section ---
# Loads credentials for all services.
# Assumes you have a .env file for local development.

# AWS GENERAL & EC2
AWS_REGION = st.secrets.get("AWS_REGION", os.getenv("AWS_REGION"))
AWS_KEY_NAME = st.secrets.get("AWS_KEY_NAME", os.getenv("AWS_KEY_NAME"))
AWS_SECURITY_GROUP_ID = st.secrets.get("AWS_SECURITY_GROUP_ID", os.getenv("AWS_SECURITY_GROUP_ID"))
AWS_AMI_ID = st.secrets.get("AWS_AMI_ID", os.getenv("AWS_AMI_ID", "ami-0d0ad8bb301edb745"))
AWS_INSTANCE_TYPE = st.secrets.get("AWS_INSTANCE_TYPE", os.getenv("AWS_INSTANCE_TYPE", "t2.micro"))
# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are found automatically by boto3 from the .env file

# AWS S3-SPECIFIC
S3_BUCKET_NAME = "*******"
S3_ACCESS_KEY_ID = "**********"
S3_SECRET_ACCESS_KEY = "***********"

# OTHER SERVICES
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
TWILIO_ACCOUNT_SID = st.secrets.get("TWILIO_ACCOUNT_SID", os.getenv("TWILIO_ACCOUNT_SID"))
TWILIO_AUTH_TOKEN = st.secrets.get("TWILIO_AUTH_TOKEN", os.getenv("TWILIO_AUTH_TOKEN"))
TWILIO_PHONE = st.secrets.get("TWILIO_PHONE_NUMBER", os.getenv("TWILIO_PHONE_NUMBER"))
LINKEDIN_ACCESS_TOKEN = st.secrets.get("LINKEDIN_ACCESS_TOKEN", os.getenv("LINKEDIN_ACCESS_TOKEN"))
LINKEDIN_URN = st.secrets.get("LINKEDIN_URN", os.getenv("LINKEDIN_URN"))
TWITTER_API_KEY = st.secrets.get("TWITTER_API_KEY", os.getenv("TWITTER_API_KEY"))
TWITTER_API_SECRET = st.secrets.get("TWITTER_API_SECRET", os.getenv("TWITTER_API_SECRET"))
TWITTER_ACCESS_TOKEN = st.secrets.get("TWITTER_ACCESS_TOKEN", os.getenv("TWITTER_ACCESS_TOKEN"))
TWITTER_ACCESS_SECRET = st.secrets.get("TWITTER_ACCESS_SECRET", os.getenv("TWITTER_ACCESS_SECRET"))
EMAIL_USERNAME = st.secrets.get("EMAIL_USERNAME", os.getenv("EMAIL_USERNAME"))
EMAIL_APP_PASSWORD = st.secrets.get("EMAIL_APP_PASSWORD", os.getenv("EMAIL_APP_PASSWORD"))


# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Unified Automation Dashboard", page_icon="🛠️", layout="wide")
st.title("🚀 Unified Automation Dashboard")
st.markdown("All your automation tools in one place: AWS, AI, Messaging, Social Media, Web & Image Utilities.")

# --- Sidebar Navigation ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", [
    "AWS Cloud Management",
    "System & Docker Automation",
    "AI Book Suggestor",
    "Messaging Tools",
    "Social Media Automation",
    "Web Utilities",
    "Image Utilities",
    "Browser-Based Tools",
    "Python Insights"
])

# --- Initialize Session State for AWS ---
if 'aws_instance_id' not in st.session_state:
    st.session_state.aws_instance_id = None
if 'aws_public_ip' not in st.session_state:
    st.session_state.aws_public_ip = None

# --- Main Page Logic ---

if page == "AWS Cloud Management":
    st.header("AWS Cloud Management ☁️")
    st.markdown("Launch instances, upload files to S3, and control services with gestures.")
    
    tab1, tab2, tab3 = st.tabs(["EC2 Instance Control", "S3 File Uploader", "Hand Gesture Control (Beta)"])

    # Uses default AWS credentials (AWS_ACCESS_KEY_ID, etc.)
    with tab1:
        st.subheader("🖥️ EC2 Instance Management")
        if not boto3:
            st.error("boto3 library not found.")
        elif not all([os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY"), AWS_KEY_NAME, AWS_SECURITY_GROUP_ID]):
            st.error("Primary AWS EC2 credentials are not fully configured. Check your .env file.")
        else:
            try:
                ec2 = boto3.client("ec2", region_name=AWS_REGION)

                def get_public_ip(instance_id):
                    try:
                        desc = ec2.describe_instances(InstanceIds=[instance_id])
                        return desc['Reservations'][0]['Instances'][0].get('PublicIpAddress')
                    except ClientError: return None

                if st.session_state.aws_instance_id:
                    st.success(f"An instance is currently running.")
                    st.code(f"Instance ID: {st.session_state.aws_instance_id}", language=None)
                    if st.session_state.aws_public_ip:
                        st.code(f"Public IP: {st.session_state.aws_public_ip}", language=None)
                    else: st.info("Public IP not yet assigned...")

                    if st.button("🚨 Terminate Instance", key="terminate_ec2"):
                        with st.spinner("Terminating instance..."):
                            ec2.terminate_instances(InstanceIds=[st.session_state.aws_instance_id])
                            waiter = ec2.get_waiter('instance_terminated')
                            waiter.wait(InstanceIds=[st.session_state.aws_instance_id])
                            st.success("✅ Instance terminated.")
                            st.session_state.aws_instance_id = None
                            st.session_state.aws_public_ip = None
                            st.rerun()
                else:
                    st.subheader("Launch New EC2 Instance")
                    if st.button("🚀 Launch Instance", type="primary", key="launch_ec2"):
                         with st.spinner("Launching instance..."):
                            response = ec2.run_instances(
                                ImageId=AWS_AMI_ID, InstanceType=AWS_INSTANCE_TYPE,
                                KeyName=AWS_KEY_NAME, MaxCount=1, MinCount=1,
                                SecurityGroupIds=[AWS_SECURITY_GROUP_ID],
                                TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'Streamlit-Dashboard-Instance'}]}]
                            )
                            instance_id = response['Instances'][0]['InstanceId']
                            st.session_state.aws_instance_id = instance_id
                            waiter = ec2.get_waiter('instance_running')
                            waiter.wait(InstanceIds=[instance_id])
                            st.session_state.aws_public_ip = get_public_ip(instance_id)
                            st.success("✅ Instance launched.")
                            st.rerun()

            except Exception as e:
                st.error(f"EC2 Error: {e}")

    # Uses dedicated S3 credentials (S3_ACCESS_KEY_ID, etc.)
    with tab2:
        st.subheader("📤 Upload Files to S3 Bucket")
        
        if not all([S3_BUCKET_NAME, S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY]):
            st.error("S3 configuration is incomplete. Ensure `S3_BUCKET_NAME`, `S3_ACCESS_KEY_ID`, and `S3_SECRET_ACCESS_KEY` are in your .env file.")
        else:
            st.info(f"Target Bucket: `{S3_BUCKET_NAME}`")
            uploaded_file = st.file_uploader("📁 Choose a file to upload", key="s3_upload")

            if uploaded_file is not None:
                if st.button("🚀 Upload to S3"):
                    try:
                        s3_client = boto3.client(
                            's3',
                            aws_access_key_id=S3_ACCESS_KEY_ID,
                            aws_secret_access_key=S3_SECRET_ACCESS_KEY,
                            region_name=AWS_REGION
                        )
                        with st.spinner(f"Uploading {uploaded_file.name}..."):
                            s3_client.upload_fileobj(uploaded_file, S3_BUCKET_NAME, uploaded_file.name)
                        st.success(f"✅ File '{uploaded_file.name}' uploaded successfully to '{S3_BUCKET_NAME}'!")
                    except ClientError as e:
                        st.error(f"❌ AWS S3 Error: {e}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {e}")

    # Uses default AWS credentials
    with tab3:
        st.subheader("🖐️ AWS Control via Hand Gestures")
        st.warning("EXPERIMENTAL: This tool uses your webcam. Performance may vary.")
        
        if not all([cv2, mp, webrtc_streamer]):
            st.error("Required libraries (OpenCV, MediaPipe, streamlit-webrtc) are not installed.")
        else:
            class AWSGestureController(VideoTransformerBase):
                def __init__(self):
                    self.hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
                    self.ec2_client = boto3.client('ec2', region_name=AWS_REGION)
                    self.last_action_time = 0
                    self.last_finger_count = -1

                def _launch_instances(self, count):
                    st.toast(f"🖐️ Launching {count} instance(s)...")
                    try:
                        self.ec2_client.run_instances(
                            ImageId=AWS_AMI_ID, InstanceType=AWS_INSTANCE_TYPE,
                            MinCount=count, MaxCount=count, KeyName=AWS_KEY_NAME,
                            SecurityGroupIds=[AWS_SECURITY_GROUP_ID]
                        )
                    except Exception as e:
                        st.toast(f"Error launching: {e}")

                def _stop_all_instances(self):
                    st.toast("✊ Stopping all instances...")
                    try:
                        instances = self.ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
                        instance_ids = [i['InstanceId'] for r in instances['Reservations'] for i in r['Instances']]
                        if instance_ids:
                            self.ec2_client.stop_instances(InstanceIds=instance_ids)
                        else: st.toast("No running instances found.")
                    except Exception as e:
                        st.toast(f"Error stopping: {e}")

                def transform(self, frame):
                    img = frame.to_ndarray(format="bgr24")
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    results = self.hands.process(img_rgb)
                    finger_count = 0

                    if results.multi_hand_landmarks:
                        hand = results.multi_hand_landmarks[0]
                        landmarks = hand.landmark
                        # Simple finger counting logic
                        finger_count += 1 if landmarks[4].x < landmarks[3].x else 0  # Thumb
                        finger_count += 1 if landmarks[8].y < landmarks[6].y else 0
                        finger_count += 1 if landmarks[12].y < landmarks[10].y else 0
                        finger_count += 1 if landmarks[16].y < landmarks[14].y else 0
                        finger_count += 1 if landmarks[20].y < landmarks[18].y else 0
                        mp.solutions.drawing_utils.draw_landmarks(img, hand, mp.solutions.hands.HAND_CONNECTIONS)
                    
                    cv2.putText(img, f'Fingers: {finger_count}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    current_time = time.time()
                    if current_time - self.last_action_time > 5 and finger_count != self.last_finger_count:
                        if 1 <= finger_count <= 5: self._launch_instances(finger_count)
                        elif finger_count == 0: self._stop_all_instances()
                        self.last_action_time = current_time
                        self.last_finger_count = finger_count
                    return img
            webrtc_streamer(key="gesture-control", video_transformer_factory=AWSGestureController, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

elif page == "System & Docker Automation":
    st.header("🖥️ System & Docker Automation Panel")
    st.info("Monitor system resources, manage Docker, and run commands both locally and remotely.")

    if not all([psutil, shutil, docker, paramiko]):
        st.error("One or more required libraries for this page are missing.")
    else:
        st.subheader("📊 System Monitor")
        col1, col2 = st.columns(2)
        with col1: st.metric("CPU Usage", f"{psutil.cpu_percent()}%")
        with col2: st.metric("RAM Usage", f"{psutil.virtual_memory().percent}%")
        
        st.subheader("🗂️ Folder Backup")
        backup_path = st.text_input("Enter folder path to backup:")
        if st.button("Create Backup"):
            backup_dir = "backups"
            if not os.path.exists(backup_dir): os.makedirs(backup_dir)
            if os.path.exists(backup_path):
                folder_name = os.path.basename(os.path.normpath(backup_path))
                time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                destination = os.path.join(backup_dir, f"{folder_name}_{time_stamp}")
                shutil.copytree(backup_path, destination)
                st.success(f"Backup created at `{destination}`")
            else: st.error("Invalid folder path!")

        st.subheader("🐳 Docker Control Panel")
        try:
            client = docker.from_env()
            containers = client.containers.list(all=True)
            if not containers: st.info("No Docker containers found.")
            else:
                for container in containers:
                    c_col1, c_col2, c_col3, c_col4 = st.columns([4, 2, 2, 2])
                    with c_col1: st.text(f"{container.short_id} - {container.name} ({container.status})")
                    with c_col2:
                        if container.status != 'running' and st.button("Start", key=f"start_{container.id}"):
                            container.start(); st.success(f"Started {container.short_id}"); st.rerun()
                    with c_col3:
                        if container.status == 'running' and st.button("Stop", key=f"stop_{container.id}"):
                            container.stop(); st.warning(f"Stopped {container.short_id}"); st.rerun()
                    with c_col4:
                         if st.button("Remove", key=f"remove_{container.id}"):
                            try:
                                container.remove(force=True); st.error(f"Removed {container.short_id}"); st.rerun()
                            except Exception as e: st.error(f"Failed to remove: {e}")
        except Exception as e:
            st.error(f"Error connecting to Docker Daemon: {e}")
            
        local_tab, ssh_tab = st.tabs(["⚡ Run Local Shell Command", "🔐 Remote SSH Command"])
        with local_tab:
            local_command = st.text_input("Enter a local command", placeholder="e.g., ls -l or dir")
            if st.button("Execute Locally"):
                output = os.popen(local_command).read(); st.code(output, language="bash")
        with ssh_tab:
            with st.form("ssh_form"):
                ssh_host, ssh_port = st.text_input("Host IP"), st.number_input("Port", value=22)
                ssh_user, ssh_password = st.text_input("Username"), st.text_input("Password", type="password")
                ssh_command = st.text_area("Command")
                if st.form_submit_button("Run via SSH"):
                    if not all([ssh_host, ssh_user, ssh_password, ssh_command]):
                        st.warning("Please fill in all SSH details.")
                    else:
                        with st.spinner(f"Connecting to {ssh_host}..."):
                            try:
                                ssh = paramiko.SSHClient(); ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                ssh.connect(ssh_host, port=ssh_port, username=ssh_user, password=ssh_password, timeout=10)
                                stdin, stdout, stderr = ssh.exec_command(ssh_command)
                                output, error = stdout.read().decode().strip(), stderr.read().decode().strip()
                                ssh.close()
                                if output: st.subheader("✅ Output:"); st.code(output, language="bash")
                                if error: st.subheader("❌ Error:"); st.code(error, language="bash")
                                if not output and not error: st.info("Command executed with no output.")
                            except Exception as e: st.error(f"SSH Error: {e}")

elif page == "AI Book Suggestor":
    st.header("📚 AI Book Suggestor")
    st.markdown("Get personalized book recommendations powered by **Google Gemini AI**.")
    if not genai:
        st.error("The `google-generativeai` library is not installed.")
    elif not GEMINI_API_KEY:
        st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
    else:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            def get_book_recommendation(genre, extra_input, reading_level, length_preference):
                system_instruction = "You are an expert literary critic... Respond ONLY with Markdown..."
                user_prompt = f"Suggest a book...\n- Genre: {genre}...\n- Notes: {extra_input if extra_input.strip() else 'None'}"
                model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_instruction)
                response = model.generate_content(user_prompt)
                return response.text.strip()
            genre = st.selectbox("🎯 Primary Genre", ["📈 Motivational", "⏳ Discipline", "..."])
            extra_input = st.text_area("🎯 Extra Preferences", placeholder="e.g., 'Female protagonist'...")
            if st.button("📖 Get Recommendation", type="primary"):
                with st.spinner("Fetching a great book for you..."):
                    result = get_book_recommendation(genre, extra_input, "General Audience", "Any Length")
                    st.markdown("### 🎁 Your AI-Picked Book"); st.markdown(result)
        except Exception as e:
            st.error(f"❌ Failed to fetch recommendation: {e}")

elif page == "Messaging Tools":
    st.header("Communication Hub 💬")
    st.markdown("Send SMS, WhatsApp, and Emails directly from here.")
    sms_tab, whatsapp_tab, email_tab, call_tab = st.tabs(["SMS Sender", "WhatsApp Sender", "Email Sender", "Voice Caller"])

    # --- SMS Sender (from sms.py) ---
    with sms_tab:
        st.subheader("📲 Twilio SMS Sender")
        if not Client:
            st.warning("`twilio` library not found. This feature is disabled.")
        else:
            sms_to_number = st.text_input("Recipient Phone Number (e.g., +91XXXXXXXXXX)", "+91", key="sms_to_number")
            sms_message_body = st.text_area("Your Message", "Hello from Streamlit! 🐍", key="sms_message_body")
            if st.button("Send SMS", key="send_sms_btn"):
                if not sms_to_number.strip() or not sms_message_body.strip():
                    st.warning("Please enter both the phone number and message.")
                elif not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE:
                    st.error("Twilio credentials not configured.")
                else:
                    try:
                        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                        message = client.messages.create(body=sms_message_body, from_=TWILIO_PHONE, to=sms_to_number)
                        st.success(f"✅ SMS sent successfully! SID: {message.sid}")
                    except Exception as e:
                        st.error(f"❌ Failed to send message: {e}")

    # --- WhatsApp Message Sender (from whatsapp.py) ---
    with whatsapp_tab:
        st.subheader("📱 WhatsApp Message Sender")
        if not kit:
            st.warning("`pywhatkit` library not found. This feature is disabled.")
        else:
            whatsapp_phone_now = st.text_input("Phone Number", value="+91", key="whatsapp_phone_now")
            whatsapp_message_now = st.text_area("Your Message", placeholder="Hi! 👋", key="whatsapp_msg_now")
            if st.button("Send WhatsApp Now"):
                if not re.match(r"^\+\d{10,15}$", whatsapp_phone_now) or not whatsapp_message_now.strip():
                    st.warning("Please enter a valid phone number and message.")
                else:
                    try:
                        st.info("Opening WhatsApp Web...")
                        kit.sendwhatmsg_instantly(phone_no=whatsapp_phone_now, message=whatsapp_message_now, wait_time=15, tab_close=True)
                        st.success("✅ Message sent!")
                    except Exception as e:
                        st.error(f"❌ WhatsApp automation failed: {e}")
    # --- Email Sender (from mail.py) ---
    with email_tab:
        st.subheader("📧 Send Email")
        if not EMAIL_USERNAME or not EMAIL_APP_PASSWORD:
            st.error("Email credentials not configured.")
        else:
            email_to = st.text_input("Recipient's Email:", key="email_to")
            email_subject = st.text_input("Subject:", key="email_subject")
            email_body = st.text_area("Message:", key="email_body")
            if st.button("Send Email", key="send_email_btn"):
                if not all([email_to.strip(), email_subject.strip(), email_body.strip()]):
                    st.warning("Please fill in all email fields.")
                else:
                    try:
                        msg_obj = MIMEMultipart()
                        msg_obj['From'] = EMAIL_USERNAME
                        msg_obj['To'] = email_to
                        msg_obj['Subject'] = email_subject
                        msg_obj.attach(MIMEText(email_body, 'plain'))
                        with smtplib.SMTP("smtp.gmail.com", 587) as server:
                            server.starttls()
                            server.login(EMAIL_USERNAME, EMAIL_APP_PASSWORD)
                            server.send_message(msg_obj)
                        st.success("✅ Email sent successfully!")
                    except Exception as e:
                        st.error(f"❌ Failed to send email: {e}")
    # --- Twilio Voice Caller (from twilio_call_app.py) ---
    with call_tab:
        st.subheader("📞 Twilio Voice Caller")
        if not Client:
            st.warning("`twilio` library not found. This feature is disabled.")
        else:
            call_to_number = st.text_input("Recipient Phone Number", "+91", key="call_to_number")
            if st.button("📞 Call Now", key="call_now_btn"):
                if not call_to_number.strip():
                    st.warning("Please enter a phone number.")
                elif not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE:
                    st.error("Twilio credentials not configured.")
                else:
                    try:
                        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                        call = client.calls.create(to=call_to_number, from_=TWILIO_PHONE, url="http://demo.twilio.com/docs/voice.xml")
                        st.success(f"✅ Call initiated! SID: {call.sid}")
                    except Exception as e:
                        st.error(f"❌ Failed to initiate call: {e}")

elif page == "Social Media Automation":
    st.header("Social Media Manager 📣")
    st.markdown("Automate your posts to Twitter, LinkedIn, and Instagram.")
    twitter_tab, linkedin_tab, instagram_tab = st.tabs(["🐦 Twitter Poster", "💼 LinkedIn Poster", "📸 Instagram Poster"])

    with twitter_tab:
        st.subheader("Post to Twitter")
        if not tweepy: st.warning("`tweepy` library not found. This feature is disabled.")
        elif not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]): st.error("Twitter API credentials not configured.")
        else:
            tweet_content = st.text_area("Tweet Content", max_chars=280, key="tweet_content")
            if st.button("Post Tweet"):
                if not tweet_content.strip(): st.warning("Tweet cannot be empty.")
                else:
                    try:
                        client_v2 = tweepy.Client(consumer_key=TWITTER_API_KEY, consumer_secret=TWITTER_API_SECRET, access_token=TWITTER_ACCESS_TOKEN, access_token_secret=TWITTER_ACCESS_SECRET)
                        client_v2.create_tweet(text=tweet_content)
                        st.success("✅ Tweet posted successfully!")
                    except Exception as e: st.error(f"Twitter error: {e}")

    with linkedin_tab:
        st.subheader("Post to LinkedIn")
        if not LINKEDIN_ACCESS_TOKEN or not LINKEDIN_URN: st.error("LinkedIn API credentials not configured.")
        else:
            linkedin_message = st.text_area("Your LinkedIn Post", "Hello, LinkedIn! #Automation #Python", key="linkedin_message")
            if st.button("Post to LinkedIn"):
                if not linkedin_message.strip(): st.warning("Post cannot be empty.")
                else:
                    headers = {"Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}", "Content-Type": "application/json"}
                    post_data = {"author": f"urn:li:person:{LINKEDIN_URN}", "lifecycleState": "PUBLISHED", "specificContent": {"com.linkedin.ugc.ShareContent": {"shareCommentary": {"text": linkedin_message},"shareMediaCategory": "NONE"}},"visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}}
                    response = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, json=post_data)
                    if response.status_code == 201: st.success("✅ Post published successfully!")
                    else: st.error(f"❌ Failed to post. Status: {response.status_code}\n{response.text}")

    with instagram_tab:
        st.subheader("Post on Instagram")
        st.markdown("Note: This uses direct login. For security, it's best to run this locally and not on a public server.")
        if not InstaClient:
            st.warning("`instagrapi` library not found. This feature is disabled. Please run `pip install instagrapi`.")
        else:
            # User credentials
            insta_username = st.text_input("Instagram Username", key="insta_user")
            insta_password = st.text_input("Instagram Password", type="password", key="insta_pass")

            # Post content
            insta_caption = st.text_area("Post Caption", key="insta_caption")
            uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], key="insta_file")

            if st.button("Post to Instagram"):
                if not insta_username or not insta_password or not uploaded_file:
                    st.warning("⚠️ Please fill in all fields.")
                else:
                    with st.spinner("Logging in and posting..."):
                        try:
                            # Save the uploaded file temporarily
                            temp_image_path = "temp_insta_post.jpg"
                            with open(temp_image_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())

                            # Login and upload
                            cl = InstaClient()
                            cl.login(insta_username, insta_password)
                            cl.photo_upload(temp_image_path, insta_caption)

                            # Cleanup
                            os.remove(temp_image_path)
                            st.success("✅ Post uploaded successfully!")

                        except Exception as e:
                            st.error(f"❌ Failed to post: {e}")


elif page == "Web Utilities":
    st.header("Web & Network Tools 🌐")
    st.subheader("🌐 Website Data Downloader")
    website_url = st.text_input("🔗 Enter Website URL", placeholder="https://example.com")
    if st.button("📥 Download Website Data"):
        if not website_url: st.warning("Please enter a URL.")
        else:
            try:
                response = requests.get(website_url)
                response.raise_for_status()
                filename = f"{urlparse(website_url).netloc.replace('.', '_')}.html"
                st.download_button("📄 Download HTML File", response.content, file_name=filename, mime="text/html")
                st.success("✅ Download prepared!")
            except Exception as e: st.error(f"❌ Failed to download website: {e}")

elif page == "Image Utilities":
    st.header("Image Generation 🖼️")
    text_input = st.text_input("Enter text for the image:", "Hello, Digital World!")
    if st.button("Generate Image"):
        image = Image.new("RGB", (800, 400), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        try:
            # On Streamlit Cloud, default fonts are limited. Provide a fallback.
            font = ImageFont.truetype("DejaVuSans.ttf", size=40)
        except IOError:
            st.warning("Default font not found, using basic font.")
            font = ImageFont.load_default()

        draw.rectangle([(50, 50), (750, 350)], outline="blue", width=5)
        draw.ellipse([(300, 100), (500, 300)], fill="lightblue", outline="black")
        text_bbox = draw.textbbox((0, 0), text_input, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        draw.text(((800 - text_width) // 2, (400 - text_height) // 2), text_input, fill="black", font=font)

        buf = io.BytesIO()
        image.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Custom Generated Image")
        st.download_button("Download Image", buf.getvalue(), "generated_image.png", "image/png")

# --- START OF NEWLY ADDED SECTION FOR BROWSER TOOLS ---
elif page == "Browser-Based Tools":
    st.header("🛠️ Browser-Based Tools")
    st.markdown("A collection of interactive tools that run directly in your browser using JavaScript. These tools may ask for permissions (like location or camera access) to function.")

    # Helper function to read and render HTML files
    def render_html_file(filepath, height):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_code = f.read()
            components.html(html_code, height=height, scrolling=True)
        except FileNotFoundError:
            st.error(f"Error: The file '{os.path.basename(filepath)}' was not found. Please make sure it's in the same directory as app.py.")

    # Create tabs for each tool
    tab_list = [
        "🗺️ Directions Finder",
        "🛒 Grocery Store Finder",
        "📈 Product Tracker",
        "📸 Photo Capture",
        "📍 Live Location",
        "📧 Email Sender",
        "🌐 IP Info"
    ]
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(tab_list)

    with tab1:
        st.subheader("Get Directions Between Two Locations")
        st.info("This tool opens Google Maps in a new tab with the specified route.")
        render_html_file('Directions.html', height=600)

    with tab2:
        st.subheader("Find Nearby Grocery Stores")
        st.info("Uses your browser's location to find and display nearby grocery stores on a map. Requires location permissions.")
        render_html_file('Grocery Store Finder.html', height=800)

    with tab3:
        st.subheader("Product Analytics Dashboard")
        st.info("An interactive dashboard to track product engagement. Data is stored in your browser's local storage.")
        render_html_file('product-tracker.html', height=800)

    with tab4:
        st.subheader("Capture Photo from Webcam")
        st.info("Uses your device's camera to capture and save a photo. Requires camera permissions.")
        render_html_file('photo.html', height=650)

    with tab5:
        st.subheader("View Your Live Location")
        st.info("Continuously tracks and displays your geographic coordinates. Requires location permissions.")
        render_html_file('Live Location1.html', height=400)

    with tab6:
        st.subheader("Pre-fill an Email")
        st.info("This tool uses a 'mailto:' link to open your computer's default email application with pre-filled content.")
        render_html_file('email.html', height=650)

    with tab7:
        st.subheader("Get Your Public IP Information")
        st.info("Fetches and displays your public IP address and approximate location.")
        render_html_file('IP info.html', height=300)
# --- END OF NEWLY ADDED SECTION ---

elif page == "Python Insights":
    st.header("Python Performance Insights 📊")
    st.subheader("Memory Comparison: List vs Tuple")
    list_obj, tuple_obj = [1, 2, "a", True], (1, 2, "a", True)
    col1, col2 = st.columns(2)
    with col1: st.metric("List size (bytes)", sys.getsizeof(list_obj))
    with col2: st.metric("Tuple size (bytes)", sys.getsizeof(tuple_obj))
    st.info("💡 Tuples are generally more memory-efficient as they are immutable.")

st.sidebar.markdown("---")
st.sidebar.caption("Built with ❤️ using Python & Streamlit.")
