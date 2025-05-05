# main.py

import os
from datetime import datetime

from src.etl.fetch_nouvelair_data import NouvelairDataFetcher
from src.etl.clean_data import clean_flight_data, status_delay_data, avg_dep_data
from src.etl.load_to_csv import save_data_to_csv
from src.etl.extract_from_csv import extract_data_from_csv
from src.etl.load_to_postgres import load_to_postgres
from src.etl.extract_from_postgres import extract_from_postgres
from src.analysis.analyze_delays import top_delayed_routes, plot_hourly_avg_delays, plot_top_delayed_routes
from src.analysis.image_analyze import generate_report_image
from src.post.generate_post import generate_post_text
from src.post.post_to_discord import post_to_discord
from src.post.post_to_X import post_to_x



# ========== ⚙️ CONFIGURATION ==========

USE_POSTGRES = False   # 🔥 Set to True if you want to practice with PostgreSQL
USE_CSV = True         # 🔥 Always keep True to store CSV

SKYFONT = os.path.abspath("src/fonts/LEDBDREV.TTF")
SKYFONT_INVERTED = os.path.abspath("src/fonts/LEDBOARD.TTF")
GLYPH_AIRPORT = os.path.abspath("src/fonts/GlyphyxOneNF.ttf")

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# ========================================

def path_dir(sub_path):
    """Create an absolute path from current directory."""
    return os.path.join(os.path.abspath(os.curdir), sub_path)

def save_or_upload_data(df, table_name):
    """Save to CSV and/or Postgres depending on config."""
    if USE_CSV:
        save_data_to_csv(df, table_name)
    if USE_POSTGRES:
        load_to_postgres(df, table_name)

if __name__ == "__main__":
    
    today_str = datetime.today().strftime('%Y_%m_%d')

    # ========== 1️⃣ Fetch Data ==========
    print("📥 Fetching Nouvelair flight data...")
    module = NouvelairDataFetcher()
    data_api = module.fetch_data()
    data_api = module.fetch_data()
    if data_api.empty:
        text = "⚠️ No data to process. Exiting script."
        print(text)
        post_to_discord(text)
        exit()

    print(data_api)

    table_name_raw = f"raw_flight_data_{today_str}"
    save_or_upload_data(data_api, table_name_raw)

    # ========== 2️⃣ Extract Raw Data ==========
    print("📤 Extracting raw data...")
    if USE_CSV:
        data = extract_data_from_csv(table_name_raw)
    else:
        data = extract_from_postgres(f"SELECT * FROM {table_name_raw}")

    # ========== 3️⃣ Clean Data ==========
    print("🧹 Cleaning data...")
    df_cleaned = clean_flight_data(data)
    df_status_cleaned = status_delay_data(data)
    df_avg_data = avg_dep_data(df_cleaned)

    table_name_cleaned = f"cleaned_flight_data_{today_str}"
    table_name_status = f"cleaned_status_delay_{today_str}"
    table_name_avg = f"cleaned_avg_hourly_{today_str}"

    save_or_upload_data(df_cleaned, table_name_cleaned)
    save_or_upload_data(df_status_cleaned, table_name_status)
    save_or_upload_data(df_avg_data, table_name_avg)

    # ========== 4️⃣ Analyze & Generate Plots ==========
    print("📊 Analyzing data and generating plots...")
    data_routes = top_delayed_routes(df_cleaned, top_n=10)

    top_delay_path = "dashboard/top_delay_plot.png"
    hourly_delay_path = "dashboard/hourly_delay_plot.png"
    plot_top_delayed_routes(data_routes, SKYFONT, top_delay_path)
    plot_hourly_avg_delays(df_avg_data, SKYFONT, hourly_delay_path)

    # ========== 5️⃣ Generate Image Report ==========
    print("🖼 Generating image report...")
    path_image, worst_flight = generate_report_image(
        df_cleaned,
        df_status_cleaned,
        top_delay_path,
        hourly_delay_path,
        SKYFONT
    )

    # ========== 6️⃣ Create Post & Publish ==========
    print("✉️ Generating post text and publishing to Discord...")
    text = generate_post_text(df_cleaned, worst_flight)
    post_to_discord(text, path_image)
    


    print("✅ Daily report generation and posting completed!")
