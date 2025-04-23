import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv
import os
# from load_to_postgres import load_to_postgres  # make sure the path is correct
# from fetch_nouvelair_data import NouvelairDataFetcher

def clean_flight_data(df):
    # with open(file_path, 'r') as file:
    #     raw_data = json.load(file)

    # df = pd.json_normalize(raw_data['data'])

    # Map and rename relevant columns
    column_mapping = {
        # 'flight_status': 'flight_status',
        'flight.iata': 'flight_iata',
        'flight_date': 'flight_date',
        'departure.airport': 'departure_airport',
        'departure.scheduled' : 'departure_scheduled' ,
        'departure.estimated': 'departure_estimated',
        'departure.actual': 'departure_actual',
        'departure.delay': 'departure_delay',
        'arrival.airport': 'arrival_airport',
        'arrival.scheduled' : 'arrival_scheduled' ,
        'arrival.estimated': 'arrival_estimated',
        'arrival.actual': 'arrival_actual',
        'arrival.delay': 'arrival_delay',
        'live.updated' : 'live_updated'
    }
    df_cleaned = df[list(column_mapping.keys())].rename(columns=column_mapping)

    # Drop rows with missing delay values
    df_cleaned = df_cleaned.dropna(subset=['departure_delay'])
    df_cleaned = df_cleaned.dropna(subset=['arrival_delay'])
    # df_cleaned = df_cleaned.dropna(subset=['flight_status'])
    # df_cleaned['arrival_delay'] = df_cleaned['arrival_delay'].fillna(df_cleaned['departure_delay'])
    # Convert delay fields to numeric
    df_cleaned['departure_delay'] = pd.to_numeric(df_cleaned['departure_delay'], errors='coerce')
    df_cleaned['arrival_delay'] = pd.to_numeric(df_cleaned['arrival_delay'], errors='coerce')

    # Add computed columns
    df_cleaned['total_delay'] = df_cleaned['departure_delay'] + df_cleaned['arrival_delay']
    df_cleaned['delay_status'] = df_cleaned['total_delay'].apply(lambda x: 'Delayed' if x > 0 else 'On-time')

    # # Convert delay columns to numeric first
    # df_cleaned['departure_delay'] = pd.to_numeric(df_cleaned['departure_delay'], errors='coerce')
    # df_cleaned['arrival_delay']   = pd.to_numeric(df_cleaned['arrival_delay'],   errors='coerce')

    # # Keep‑mask:   keep if (status == 'cancelled')  OR  (at least one delay present)
    # mask_keep = (
    #     (df_cleaned['flight_status'].str.lower() == 'cancelled') |  
    #     df_cleaned[['departure_delay', 'arrival_delay']].notna().any(axis=1)
    # )

    # # Apply the mask
    # df_cleaned = df_cleaned[~mask_keep].copy()

    # # Fill arrival_delay with departure_delay if arrival missing (optional)
    # # df_cleaned['arrival_delay'] = df_cleaned['arrival_delay'].fillna(df_cleaned['departure_delay'])

    # # Total delay (treat NaNs as 0 for cancelled flights)
    # df_cleaned['total_delay'] = df_cleaned[['departure_delay', 'arrival_delay']].fillna(0).sum(axis=1)

    # # Delay status
    # df_cleaned['delay_status'] = df_cleaned['total_delay'].apply(
    #     lambda x: 'Cancelled' if pd.isna(x) else ('Delayed' if x > 0 else 'On‑time')
    # )

    return df_cleaned

def status_delay_data(df) :
    # Map and rename relevant columns
    column_mapping = {
        'flight.iata': 'flight_iata',
        'flight_date': 'flight_date',
        'flight_status': 'flight_status'
    }
    df_cleaned = df[list(column_mapping.keys())].rename(columns=column_mapping)
    df_cleaned = df_cleaned.dropna(subset=['flight_status'])

    return df_cleaned