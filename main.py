from src.etl.clean_data import clean_flight_data,status_delay_data
# from src.etl.create_tables import create_table
# from src.etl.fetch_nouvelair_data import NouvelairDataFetcher
from sqlalchemy import text
from src.etl.load_to_postgres import load_to_postgres
from src.etl.extract_from_postgres import extract_from_postgres
from datetime import datetime



if __name__ == "__main__":
    # create_table()
    # module = NouvelairDataFetcher()
    # data_api = module.fetch_data()
    table_name = f"raw_flight_data_{datetime.today().strftime('%Y_%m_%d')}"
    # load_to_postgres(data_api, table_name)
    table_name_cleaned = f"cleaned_flight_data_{datetime.today().strftime('%Y_%m_%d')}"
    table_status = f"cleaned_status_delay_{datetime.today().strftime('%Y_%m_%d')}"
    sql = text(f'SELECT * FROM {table_name}')
    data = extract_from_postgres(sql)
    df_cleaned = clean_flight_data(data)
    df_status_cleaned = status_delay_data(data)
    print(df_status_cleaned)
    load_to_postgres(df_cleaned, table_name_cleaned)
    load_to_postgres(df_status_cleaned,table_status)
