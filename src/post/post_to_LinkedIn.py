import tweepy
from dotenv import load_dotenv
import os
import requests


def post_to_linkedin(asset_id, text):
    load_dotenv()
    access_token = os.getenv("Linked_API_Key")
    page_id = os.getenv("PAGE_ID")
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    post_body = {
        "author": f"urn:li:organization:{page_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "IMAGE",
                "media": [{
                    "status": "READY",
                    "description": {"text": "Flight delay report"},
                    "media": asset_id,
                    "title": {"text": "Flight Delay Update"}
                }]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=post_body)

    if response.status_code == 201:
        print("✅ Post published successfully!")
    else:
        print(f"❌ Failed to post! Status code: {response.status_code}")
        print(f"Response: {response.text}")
        response.raise_for_status()


