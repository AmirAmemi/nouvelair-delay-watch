import os
import requests
import pandas as pd
from dotenv import load_dotenv

class NouvelairDataFetcher:
    """
    A class to fetch Nouvelair flight data from the AviationStack API.

    Attributes:
        api_key (str): AviationStack API key.
        url (str): API endpoint.
        airline_code (str): Nouvelair's IATA airline code ("BJ").
    """

    def __init__(self):
        """Initialize the fetcher by loading API key from environment variables."""
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.url = "https://api.aviationstack.com/v1/flights"
        self.airline_code = "BJ"

    def fetch_data(self):
        """
        Fetch the latest Nouvelair flight data from the AviationStack API.

        Returns:
            pd.DataFrame: A DataFrame containing Nouvelair flight data.

        Raises:
            ValueError: If the API response structure is invalid.
            requests.exceptions.HTTPError: If the API request fails.
        """
        params = {
            'access_key': self.api_key,
            'airline_iata': self.airline_code,
            'limit': 100  # Adjusted based on API plan
        }

        response = requests.get(self.url, params=params)
        response.raise_for_status()

        data = response.json()

        if 'data' in data:
            df = pd.json_normalize(data['data'])
            print("✅ Data fetched successfully from AviationStack API.")
            return df
        else:
            raise ValueError("❌ Invalid API response structure: 'data' field missing.")
