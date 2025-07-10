import requests

# Replace with your access token
ACCESS_TOKEN = 'YOUR_LINKEDIN_ACCESS_TOKEN'

# Replace with your LinkedIn user ID
LINKEDIN_URN = 'urn:li:person:YOUR_LINKEDIN_ID'

# Your message
message = """
👋 Just built something cool!

📲 WhatsApp Automation Pro – A tool to send & schedule WhatsApp messages using Python + Streamlit

Big thanks to Vimal Daga Sir and LinuxWorld Informatics Pvt. Ltd. for the mentorship and guidance. #Python #Streamlit #Automation
"""

post_data = {
    "author": LINKEDIN_URN,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": message
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "X-Restli-Protocol-Version": "2.0.0",
    "Content-Type": "application/json"
}

response = requests.post(
    'https://api.linkedin.com/v2/ugcPosts',
    headers=headers,
    json=post_data
)

if response.status_code == 201:
    print("✅ Post published successfully!")
else:
    print(f"❌ Failed to post. Status code: {response.status_code}")
    print(response.text)
