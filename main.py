from src.etl.clean_data import clean_flight_data,status_delay_data,avg_dep_data
# from src.etl.create_tables import create_table
# from src.etl.fetch_nouvelair_data import NouvelairDataFetcher
from sqlalchemy import text
from src.etl.load_to_postgres import load_to_postgres
from src.etl.extract_from_postgres import extract_from_postgres
from src.analysis.analyze_delays import flight_status_distribution,top_delayed_routes, plot_hourly_avg_delays,plot_top_delayed_routes
from src.analysis.image_analyze import generate_report_image
from datetime import datetime
import os

def path_dir(sub_path):
    """
    to create an abs path from current dir

    :param sub_path: (str), sub_path in string
    :return: (str), absolute path
    """
    assert isinstance(sub_path, str), "sub_path must be a string"
    return os.path.join(os.path.abspath(os.curdir), sub_path)

if __name__ == "__main__":
    # create_table()
    # module = NouvelairDataFetcher()
    # data_api = module.fetch_data()
    table_name = f"raw_flight_data_{datetime.today().strftime('%Y_%m_%d')}"
    # load_to_postgres(data_api, table_name)
    table_name_cleaned = f"cleaned_flight_data_{datetime.today().strftime('%Y_%m_%d')}"
    table_status = f"cleaned_status_delay_{datetime.today().strftime('%Y_%m_%d')}"
    table_avg = f"cleaned_avg_hourly_{datetime.today().strftime('%Y_%m_%d')}"
    sql = text(f'SELECT * FROM {table_name}')
    data = extract_from_postgres(sql)
    df_cleaned = clean_flight_data(data)
    df_status_cleaned = status_delay_data(data)
    df_avg_data = avg_dep_data(df_cleaned)
    # print(avg_dep_data(data))
    print(df_cleaned)
    load_to_postgres(df_cleaned, table_name_cleaned)
    load_to_postgres(df_status_cleaned,table_status)
    load_to_postgres(df_avg_data,table_avg)
    SKYFONT = path_dir("src/fonts/LEDBDREV.TTF")
    # # print(df_status_cleaned.columns)
    # # print(top_delayed_routes(df_cleaned))
    # plot_hourly_avg_delays(df_avg_data,SKYFONT)
    data_routes = top_delayed_routes(df_cleaned,10)
    
    # plot_top_delayed_routes(data_routes,SKYFONT)
    top_delay_path = "top_delay_plot.png"
    hourly_delay_path = "hourly_delay_plot.png"
    plot_top_delayed_routes(data_routes,SKYFONT,top_delay_path)
    # plot_top_delayed_routes(df_cleaned,10,top_delay_path)
    plot_hourly_avg_delays(df_avg_data,SKYFONT,hourly_delay_path)
    # plot_hourly_avg_delays(df_avg_data,SKYFONT,hourly_delay_path)
    generate_report_image(df_cleaned,df_status_cleaned,top_delay_path,hourly_delay_path)