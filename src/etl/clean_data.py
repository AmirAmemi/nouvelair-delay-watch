import pandas as pd
import json
from datetime import datetime

def load_raw_data(filename):
    
    with open(filename,'r') as file :
        return json.load(file)
file = f"data/raw_flights_{datetime.today().strftime('%Y-%m-%d')}.json"
raw_data = load_raw_data(file)

df = pd.json_normalize(raw_data['data'])

# Columns we need
relevant_columns = [
    'flight_status','flight_date', 'flight.iata', 'departure.airport', 'departure.estimated', 
    'arrival.airport', 'arrival.estimated', 'flight_status', 'departure.delay', 'arrival.delay'
]

# Keep only relevant columns
df_cleaned = df[relevant_columns]

# Drop rows with missing delay values
df_cleaned = df_cleaned.dropna(subset=['departure.delay', 'arrival.delay'])

# Convert delay columns to numeric values (if they are not already)
df_cleaned['departure.delay'] = pd.to_numeric(df_cleaned['departure.delay'], errors='coerce')
df_cleaned['arrival.delay'] = pd.to_numeric(df_cleaned['arrival.delay'], errors='coerce')

# Calculate total delay
df_cleaned['total.delay'] = df_cleaned['departure.delay'] + df_cleaned['arrival.delay']

# Add a delay status column
df_cleaned['delay.status'] = df_cleaned['total.delay'].apply(lambda x: 'Delayed' if x > 0 else 'On-time')

# Save cleaned data to CSV
df_cleaned.to_csv(f'data/cleaned_flights_{datetime.today().strftime("%Y-%m-%d")}.csv', index=False)

# Optionally, save as a JSON file
df_cleaned.to_json(f'data/cleaned_flights_{datetime.today().strftime("%Y-%m-%d")}.json', orient='records', lines=True)

