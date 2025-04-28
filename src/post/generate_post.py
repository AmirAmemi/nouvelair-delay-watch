from datetime import datetime
import requests
from dotenv import load_dotenv
import os

def generate_post_text(df_cleaned,worst_flight):
    """
    Create a text for the post based on flight information.

    Parameters:
    - flight_info (dict): information like date, airline, airports, delay info, etc.

    Returns:
    - str: the generated post text.
    """
    sum_dep = df_cleaned[df_cleaned["departure_delay"] > 0].count()
    sum_arr = df_cleaned[df_cleaned["arrival_delay"] > 0].count()
    text = (
        f". \n\n✈️ #Nouvelair Flight Delay Report\n\n"
        f"📅 Date: {datetime.today().strftime('%Y-%m-%d')} \n"
        f"Total Delays :  \n"
        f"{sum_dep['departure_delay']} #DelayedDepartures\n"
        f"{sum_arr['arrival_delay']} #DelayedArrivals \n\n"
        f"⚠️ Worst Flight: \n"
        f"🛫 {worst_flight['departure_airport']} ➡️ {worst_flight['arrival_airport']} 🛬 delayed by {int(worst_flight['arrival_delay'])} minutes! 🕒\n\n"
        f"🌍 #Tunisia #Nouvelair #FlightData #AirlinePerformance #DataEngineer #DataAnalyst  "
    )
    return text


def upload_linkedin_image(image_path):
    """
    Upload an image to LinkedIn and return the asset ID.
    """
    load_dotenv()
    access_token = os.getenv("Linked_API_Key")
    page_id = os.getenv("PAGE_ID")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Step 1: Register Upload
    register_upload_url = "https://api.linkedin.com/v2/assets?action=registerUpload"

    register_upload_body = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": f"urn:li:organization:{page_id}",
            "serviceRelationships": [{
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }]
        }
    }

    response = requests.post(register_upload_url, headers=headers, json=register_upload_body)
    response.raise_for_status()

    upload_info = response.json()
    upload_url = upload_info["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
    asset_id = upload_info["value"]["asset"]

    # Step 2: Upload Image
    with open(image_path, "rb") as f:
        upload_response = requests.put(upload_url, data=f, headers={"Authorization": f"Bearer {access_token}"})
        upload_response.raise_for_status()

    return asset_id
