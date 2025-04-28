# src/etl/extract_from_csv.py

import os
import pandas as pd

def extract_data_from_csv(table_name):
    """
    Extract data from a CSV file inside the /data/ folder.

    Args:
        table_name (str): The table name (file name without .csv).

    Returns:
        pd.DataFrame: The loaded dataframe.
    """
    # Define folder and file path
    file_path = f"data/{table_name}.csv"

    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ CSV file not found: {file_path}")

    # Load CSV into DataFrame
    df = pd.read_csv(file_path)
    print(f"✅ Data extracted successfully from {file_path}")
    return df
