import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
import os
import time

class NouvelairDataFetcher:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.url = "https://api.aviationstack.com/v1/flights"
        self.airline_code = "BJ"

    def fetch_data(self):
        params = {
            'access_key': self.api_key,
            'airline_iata': self.airline_code,
            'limit': 100
        }
        response = requests.get(self.url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'data' in data:
            df = pd.json_normalize(data['data'])
            df = df[df["flight_date"] == datetime.today().strftime('%Y-%m-%d')]
            return df
        else:
            raise ValueError("Invalid API response structure")



# module = NouvelairDataFetcher()

# data = module.fetch_data()
# print(data.columns)
# load_to_postgres(data)