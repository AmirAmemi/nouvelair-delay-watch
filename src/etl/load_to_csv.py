# src/etl/load_to_csv.py

import pandas as pd

def save_data_to_csv(data, path):
    """
    Save a Pandas DataFrame to a CSV file.

    Args:
        data (pd.DataFrame): The dataframe to save.
        path (str): The full path where the CSV should be saved.

    Returns:
        None
    """
    # path = f"data/{table_name}"
    # Save to CSV
    data.to_csv(path, index=False)
    print(f"✅ Data saved successfully to {path}")
