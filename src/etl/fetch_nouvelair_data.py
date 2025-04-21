import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env
load_dotenv()

# Fetch the API key from the .env file
API_KEY = os.getenv("API_KEY")

# Check if API_KEY is loaded properly
if not API_KEY:
    raise ValueError("API_KEY not found in environment variables!")

API_URL = "http://api.aviationstack.com/v1/flights"

# Set parameters to filter for Nouvelair (IATA code: BJ)
params = {
    'access_key': API_KEY,
    'airline_iata': 'BJ',
    'limit': 100  # You can paginate if needed
}

def fetch_and_save_flights():
    print("Fetching data from AviationStack...")
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        # Create data folder if not exists
        os.makedirs('data', exist_ok=True)

        filename = f"data/raw_flights_{datetime.today().strftime('%Y-%m-%d')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        print(f"✅ Data saved to {filename}")
    else:
        print(f"❌ Failed to fetch data. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    fetch_and_save_flights()
