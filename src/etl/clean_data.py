import pandas as pd

def clean_flight_data(df):

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

    
    # Convert delay fields to numeric
    df_cleaned['departure_delay'] = pd.to_numeric(df_cleaned['departure_delay'], errors='coerce')
    df_cleaned['arrival_delay'] = pd.to_numeric(df_cleaned['arrival_delay'], errors='coerce')

    # Add computed columns
    df_cleaned['total_delay'] = df_cleaned['departure_delay'] + df_cleaned['arrival_delay']
    df_cleaned['delay_status'] = df_cleaned['total_delay'].apply(lambda x: 'Delayed' if x > 0 else 'On-time')

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
    df_cleaned['flight_status'] = df_cleaned['flight_status'].str.lower()


    return df_cleaned

def avg_dep_data(df):
    
    df_cleaned =df
    #  Ensure datetime dtype
    df_cleaned['departure_scheduled'] = pd.to_datetime(df_cleaned['departure_scheduled'])
    df_cleaned['arrival_scheduled']   = pd.to_datetime(df_cleaned['arrival_scheduled'])

    # Extract the hour (0‑23)
    df_cleaned['dep_hour'] = df_cleaned['departure_scheduled'].dt.hour
    df_cleaned['arr_hour'] = df_cleaned['arrival_scheduled'].dt.hour

    #Group‑by hour and compute the average delay (in minutes)
    avg_dep = df_cleaned.groupby('dep_hour')['departure_delay'].mean()
    avg_arr = df_cleaned.groupby('arr_hour')['arrival_delay'].mean()

   
    hours = pd.DataFrame({'hour': range(1,25)})

    hourly_delays = (
    hours
      .merge(avg_dep.rename('avg_departure_delay'), left_on='hour', right_index=True, how='left')
      .merge(avg_arr.rename('avg_arrival_delay'),   left_on='hour', right_index=True, how='left')
      .fillna(0)
      .astype({'hour': int,'avg_departure_delay':int,'avg_arrival_delay':int})
      .sort_values('hour')
      .reset_index(drop=True)
                    )
    return hourly_delays

def most_delayed_routes(df):

    return