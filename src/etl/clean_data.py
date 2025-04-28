import pandas as pd

# ---------------------------------------------------------
# Main Cleaning Function
# ---------------------------------------------------------

def clean_flight_data(df):
    """
    Clean the main flight dataset by:
    - Selecting relevant columns
    - Renaming columns
    - Dropping missing delays
    - Converting delays to numeric
    - Adding total delay and delay status columns

    Args:
        df (DataFrame): Raw flight dataset.

    Returns:
        DataFrame: Cleaned flight data ready for analysis.
    """

    column_mapping = {
        'flight.iata': 'flight_iata',
        'flight_date': 'flight_date',
        'departure.iata': 'departure_iata',
        'departure.airport': 'departure_airport',
        'departure.scheduled': 'departure_scheduled',
        'departure.estimated': 'departure_estimated',
        'departure.actual': 'departure_actual',
        'departure.delay': 'departure_delay',
        'arrival.iata': 'arrival_iata',
        'arrival.airport': 'arrival_airport',
        'arrival.scheduled': 'arrival_scheduled',
        'arrival.estimated': 'arrival_estimated',
        'arrival.actual': 'arrival_actual',
        'arrival.delay': 'arrival_delay',
        'live.updated': 'live_updated',
        'airline.name': 'airline_name',
    }

    # Select and rename columns
    df_cleaned = df[list(column_mapping.keys())].rename(columns=column_mapping)

    # Drop rows with missing delay values
    df_cleaned = df_cleaned.dropna(subset=['departure_delay', 'arrival_delay'])

    # Convert delay fields to numeric
    df_cleaned['departure_delay'] = pd.to_numeric(df_cleaned['departure_delay'], errors='coerce')
    df_cleaned['arrival_delay'] = pd.to_numeric(df_cleaned['arrival_delay'], errors='coerce')

    # Add computed columns
    df_cleaned['total_delay'] = df_cleaned['departure_delay'] + df_cleaned['arrival_delay']
    df_cleaned['delay_status'] = df_cleaned['total_delay'].apply(lambda x: 'Delayed' if x > 0 else 'On-time')

    return df_cleaned

# ---------------------------------------------------------
# Status Delay Cleaning
# ---------------------------------------------------------

def status_delay_data(df):
    """
    Extract and clean flight status information.

    Args:
        df (DataFrame): Raw flight dataset.

    Returns:
        DataFrame: Cleaned status delay information.
    """

    column_mapping = {
        'flight.iata': 'flight_iata',
        'flight_date': 'flight_date',
        'flight_status': 'flight_status'
    }

    df_status = df[list(column_mapping.keys())].rename(columns=column_mapping)

    # Drop missing status
    df_status = df_status.dropna(subset=['flight_status'])

    # Normalize status to lowercase
    df_status['flight_status'] = df_status['flight_status'].str.lower()

    return df_status

# ---------------------------------------------------------
# Average Delays Per Hour
# ---------------------------------------------------------

def avg_dep_data(df):
    """
    Calculate average departure and arrival delays for each hour of the day.

    Args:
        df (DataFrame): Cleaned flight data.

    Returns:
        DataFrame: Hourly average delays (departure & arrival).
    """

    df = df.copy()

    # Ensure datetime format
    df['departure_scheduled'] = pd.to_datetime(df['departure_scheduled'])
    df['arrival_scheduled'] = pd.to_datetime(df['arrival_scheduled'])

    # Extract hour
    df['dep_hour'] = df['departure_scheduled'].dt.hour
    df['arr_hour'] = df['arrival_scheduled'].dt.hour

    # Group by hour and compute mean delays
    avg_dep = df.groupby('dep_hour')['departure_delay'].mean()
    avg_arr = df.groupby('arr_hour')['arrival_delay'].mean()

    # Prepare full 1-24 hour DataFrame
    hours = pd.DataFrame({'hour': range(1, 25)})

    hourly_delays = (
        hours
        .merge(avg_dep.rename('avg_departure_delay'), left_on='hour', right_index=True, how='left')
        .merge(avg_arr.rename('avg_arrival_delay'), left_on='hour', right_index=True, how='left')
        .fillna(0)
        .astype({'hour': int, 'avg_departure_delay': int, 'avg_arrival_delay': int})
        .sort_values('hour')
        .reset_index(drop=True)
    )

    return hourly_delays

# ---------------------------------------------------------
# Placeholder: Most Delayed Routes (Optional)
# ---------------------------------------------------------

def most_delayed_routes(df):
    """
    [Not Implemented Yet]
    Potential function for extracting most delayed routes.

    Args:
        df (DataFrame): Flight dataset.

    Returns:
        str: Placeholder text.
    """
    return "Function not yet implemented."
