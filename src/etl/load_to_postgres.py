import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# ---------------------------------------------------------
# Load Data to PostgreSQL
# ---------------------------------------------------------

def load_to_postgres(df: pd.DataFrame, table_name: str = 'raw_flight_data') -> None:
    """
    Load a pandas DataFrame into a PostgreSQL table.

    Args:
        df (pd.DataFrame): The dataframe to load into the database.
        table_name (str): The name of the target table in PostgreSQL.

    Environment Variables Needed:
        POSTGRES_USER: Username for PostgreSQL
        POSTGRES_PASSWORD: Password for PostgreSQL
        POSTGRES_HOST: Hostname or IP address of PostgreSQL
        POSTGRES_PORT: Port number for PostgreSQL
        POSTGRES_DB: Database name for PostgreSQL

    Raises:
        sqlalchemy.exc.SQLAlchemyError: If there is an issue connecting or loading the data.
    """
    # Load environment variables
    load_dotenv()
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_HOST = os.getenv("POSTGRES_HOST")
    DB_PORT = os.getenv("POSTGRES_PORT")
    DB_NAME = os.getenv("POSTGRES_DB")

    # Create the PostgreSQL engine
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Load the dataframe to PostgreSQL
    with engine.begin() as connection:
        df.to_sql(
            table_name,
            connection,
            if_exists='replace',  # Replace the table if it exists
            index=False,
            method='multi'        # Insert multiple rows at once for better performance
        )
    print(f"✅ Data loaded successfully into PostgreSQL table: {table_name}")
