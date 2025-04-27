import requests
from dotenv import load_dotenv
import os

def post_to_discord(message_text, image_path):
    load_dotenv()
    webhook_url =  os.getenv("webhook_url")
    
    with open(image_path, "rb") as f:
        file_data = {"file": (image_path, f)}
        payload = {"content": message_text}
        response = requests.post(webhook_url, data=payload, files=file_data)

    if response.status_code in (200,204):
        print("✅ Successfully posted to Discord!")
    else:
        print(f"❌ Failed to post! Status code: {response.status_code}")
        print(f"Response: {response.text}")


