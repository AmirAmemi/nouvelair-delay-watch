import os
import pandas as pd

# ---------------------------------------------------------
# Extract Function
# ---------------------------------------------------------

def extract_data_from_csv(table_name):
    """
    Extract data from a CSV file located inside the `/data/` folder.

    Args:
        table_name (str): Name of the table (without `.csv` extension).

    Returns:
        pd.DataFrame: The loaded dataframe.

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
    """

    # Construct full file path
    file_path = f"data/{table_name}.csv"

    # Validate file existence
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ CSV file not found: {file_path}")

    # Load CSV into a DataFrame
    df = pd.read_csv(file_path)

    print(f"✅ Data extracted successfully from {file_path}")
    return df
