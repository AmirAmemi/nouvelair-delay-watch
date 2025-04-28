import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

def extract_from_postgres(sql_query):
    """
    Extract data from a PostgreSQL database based on a SQL query.

    Args:
        sql_query (str): SQL query string to execute.

    Returns:
        pd.DataFrame: The resulting data as a pandas DataFrame.

    Raises:
        ValueError: If database connection parameters are missing.
    """

    # Load environment variables
    load_dotenv()

    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_HOST = os.getenv("POSTGRES_HOST")
    DB_PORT = os.getenv("POSTGRES_PORT")
    DB_NAME = os.getenv("POSTGRES_DB")

    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
        raise ValueError("❌ Database credentials are not fully set in environment variables.")

    # Create SQLAlchemy engine
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Execute query and load into DataFrame
    with engine.connect() as conn:
        df = pd.read_sql(sql_query, conn)

    print(f"✅ Data extracted successfully from database.")
    return df
