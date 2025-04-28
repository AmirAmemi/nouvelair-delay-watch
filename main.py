from src.etl.clean_data import clean_flight_data,status_delay_data,avg_dep_data

from src.etl.fetch_nouvelair_data import NouvelairDataFetcher
from sqlalchemy import text
from src.etl.extract_from_csv import extract_data_from_csv
from src.etl.load_to_csv import save_data_to_csv
from src.etl.load_to_postgres import load_to_postgres
from src.etl.extract_from_postgres import extract_from_postgres
from src.analysis.analyze_delays import flight_status_distribution,top_delayed_routes, plot_hourly_avg_delays,plot_top_delayed_routes
from src.analysis.image_analyze import generate_report_image
from src.post.post_to_LinkedIn import post_to_linkedin
from src.post.generate_post import generate_post_text,upload_linkedin_image
from src.post.post_to_discord import post_to_discord
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
    
    module = NouvelairDataFetcher()
    data_api = module.fetch_data()
    today = datetime.today().strftime('%Y_%m_%d')
    table_name = f"raw_flight_data_{today}"
    path_table = path_dir(f"data/{table_name}.csv")
    # load_to_postgres(data_api, table_name)
    save_data_to_csv(data_api,path_table)
    table_name_cleaned = f"cleaned_flight_data_{today}"
    path_table_cleaned = path_dir(f"data/{table_name_cleaned}.csv")
    table_status = f"cleaned_status_delay_{today}"
    path_table_status = path_dir(f"data/{table_status}.csv")
    table_avg = f"cleaned_avg_hourly_{today}"
    path_table_avg = path_dir(f"data/{table_avg}.csv")
    # sql = text(f'SELECT * FROM {table_name}')
    # data = extract_from_postgres(sql)
    data =  extract_data_from_csv(path_table)
    df_cleaned = clean_flight_data(data)
    df_status_cleaned = status_delay_data(data)
    df_avg_data = avg_dep_data(df_cleaned)

    
    save_data_to_csv(df_cleaned,path_table_cleaned)
    save_data_to_csv(df_status_cleaned,path_table_status)
    save_data_to_csv(df_avg_data,path_table_avg)
    # load_to_postgres(df_cleaned, table_name_cleaned)
    # load_to_postgres(df_status_cleaned,table_status)
    # load_to_postgres(df_avg_data,table_avg)

    SKYFONT = path_dir("src/fonts/LEDBDREV.TTF")
    SKYFONT_INVERTED = path_dir("src/fonts/LEDBOARD.TTF")
    GLYPH_AIRPORT = path_dir("src/fonts/GlyphyxOneNF.ttf")
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
    path_image,worst_flight = generate_report_image(df_cleaned,df_status_cleaned,top_delay_path,hourly_delay_path,SKYFONT)
    text = generate_post_text(df_cleaned,worst_flight)
    # asset = upload_linkedin_image(path_image)
    # post_to_linkedin(asset,              text)
    post_to_discord(text,path_image)