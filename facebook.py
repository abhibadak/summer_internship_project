import requests

PAGE_ID = "your_page_id_here"
ACCESS_TOKEN = "your_page_access_token_here"

message = "🚀 Hello from Python! This post was made using Facebook Graph API."

url = f"https://graph.facebook.com/{PAGE_ID}/feed"

payload = {
    'message': message,
    'access_token': ACCESS_TOKEN
}

response = requests.post(url, data=payload)

if response.status_code == 200:
    print("✅ Post published successfully!")
    print("Post ID:", response.json().get('id'))
else:
    print("❌ Failed to post.")
    print("Status Code:", response.status_code)
    print(response.text)
