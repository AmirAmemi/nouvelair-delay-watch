# src/etl/extract_from_postgres.py

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def extract_from_postgres(sql):
    load_dotenv()
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_HOST = os.getenv("POSTGRES_HOST")
    DB_PORT = os.getenv("POSTGRES_PORT")
    DB_NAME = os.getenv("POSTGRES_DB")

    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)
    return df
