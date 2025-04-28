import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

# ---------------------------------------------------------
# Plotting Functions
# ---------------------------------------------------------

def create_simple_plot(values, labels, title, ylabel, output_path):
    """
    Create a simple bar plot and save it to disk.

    Args:
        values (list): Y-values for the bars.
        labels (list): X-labels for the bars.
        title (str): Title of the plot.
        ylabel (str): Label for the Y-axis.
        output_path (str): Path to save the plot.
    """
    plt.figure(figsize=(5, 3))
    plt.bar(labels, values, color='orange')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

# ---------------------------------------------------------
# Text Utilities
# ---------------------------------------------------------

def get_text_dimensions(text_string: str, font):
    """
    Calculate the width and height of a text string with a given font.

    Args:
        text_string (str): The text to measure.
        font (ImageFont): The font object.

    Returns:
        tuple: (text_width, text_height)
    """
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return text_width, text_height

# ---------------------------------------------------------
# Title Block
# ---------------------------------------------------------

def past_titles(draw, SKYFONT, datetime_query):
    """
    Draws the top titles (date, project name) on the report.

    Args:
        draw (ImageDraw.Draw): ImageDraw object to draw on the image.
        SKYFONT (str): Path to the font file.
        datetime_query (datetime): Current datetime object.

    Returns:
        draw (ImageDraw.Draw): Modified ImageDraw object.
    """
    draw.text(
        (55, 60),
        f"LAST UPDATE AT {datetime_query.strftime('%H:%M')}",
        font=ImageFont.truetype(SKYFONT, 9),
        fill="black",
    )
    draw.text(
        (260, 10),
        f"NOUVELAIR DAILY INGEST {datetime_query.strftime('%a %d %B %Y').upper()}",
        font=ImageFont.truetype(SKYFONT, 25),
        fill="black",
    )
    draw.text(
        (260, 50),
        "NOUVELAIR FLIGHT DELAY ANALYSIS REPORT",
        font=ImageFont.truetype(SKYFONT, 15),
        fill="black",
    )
    return draw

# ---------------------------------------------------------
# Main Dashboard Generation
# ---------------------------------------------------------

def generate_report_image(df, df_st, top_delay_path, hourly_delay_path, SKYFONT, output_path="dashboard/final_report.png"):
    """
    Generate a daily report dashboard as an image.

    Args:
        df (DataFrame): Cleaned flight data.
        df_st (DataFrame): Status distribution data.
        top_delay_path (str): Path to saved Top Delayed Routes plot.
        hourly_delay_path (str): Path to saved Hourly Delay plot.
        SKYFONT (str): Path to font file.
        output_path (str, optional): Final output path. Defaults to "dashboard/final_report.png".

    Returns:
        tuple: (output_path, worst_flight)
    """

    report_img = Image.new("RGB", (1080, 720), color="black")

    # Load Logo
    logo_path = "src/analysis/nouvelair_logo.png"
    if os.path.exists(logo_path):
        with Image.open(logo_path) as logo:
            report_img.paste(logo, (0, 0))
    else:
        print(f"Logo not found at {logo_path}")

    draw = ImageDraw.Draw(report_img)
    date_now = datetime.now()
    past_titles(draw, SKYFONT, date_now)

    font = ImageFont.truetype(SKYFONT, size=17)

    # KPIs Calculation
    flight_status_counts = df_st['flight_status'].value_counts()
    scheduled = flight_status_counts.get('scheduled', 0)
    canceled = flight_status_counts.get('cancelled', 0)
    active = flight_status_counts.get('active', 0)
    landed = flight_status_counts.get('landed', 0)

    dep_delays = df['departure_delay'].dropna()
    arr_delays = df['arrival_delay'].dropna()

    dep_stats = [int(dep_delays.min()), int(dep_delays.max()), int(dep_delays.mean()), int(dep_delays.sum())]
    arr_stats = [int(arr_delays.min()), int(arr_delays.max()), int(arr_delays.mean()), int(arr_delays.sum())]

    worst_flight = df.loc[df['arrival_delay'].idxmax()]

    # Draw KPIs
    kpi_texts = [
        f"NOUVELAIR FLIGHTS       SCHEDULED: {scheduled}     CANCELLED: {canceled}     ACTIVE: {active}     LANDED: {landed}"
    ]
    stats_dep_text = [f"DELAYED DEPARTURE: {int(dep_stats[3]/60)}H",
                      f"MIN: {dep_stats[0]}M   MAX: {dep_stats[1]}M   AVG: {dep_stats[2]}M"]
    stats_arr_text = [f"DELAYED ARRIVAL: {int(arr_stats[3]/60)}H",
                      f"MIN: {arr_stats[0]}M   MAX: {arr_stats[1]}M   AVG: {arr_stats[2]}M"]

    worst_flight_text = [
        f"WORST FLIGHT:",
        f"{worst_flight['airline_name']} {worst_flight['flight_iata']}",
        f"{worst_flight['departure_airport']} ----- DELAY OF {int(worst_flight['arrival_delay'] + worst_flight['departure_delay'])} MIN -----> {worst_flight['arrival_airport']}"
    ]

    # Draw KPI Texts
    for idx, text in enumerate(kpi_texts):
        draw.text((30, 120 + idx * 30), text, font=ImageFont.truetype(SKYFONT, 15), fill="white")

    for idx, text in enumerate(stats_dep_text):
        draw.text((80, 170 + idx * 30), text, font=ImageFont.truetype(SKYFONT, 15), fill="white")
    
    for idx, text in enumerate(stats_arr_text):
        draw.text((600, 170 + idx * 30), text, font=ImageFont.truetype(SKYFONT, 15), fill="white")

    # Draw Worst Flight
    draw.text((300, 235), worst_flight_text[0], font=ImageFont.truetype(SKYFONT, 14), fill="#447add")
    draw.text((480, 235), worst_flight_text[1], font=ImageFont.truetype(SKYFONT, 14), fill="white")
    draw.text((270, 265), worst_flight_text[2], font=ImageFont.truetype(SKYFONT, 14), fill="white")

    # Draw Graphs
    hourly_delay = Image.open(hourly_delay_path)
    top_delay = Image.open(top_delay_path)

    report_img.paste(hourly_delay, (50, 290))
    report_img.paste(top_delay, (50, 490))

    # Draw Rectangles
    draw.rounded_rectangle([(30, 310), (1000, 680)], radius=15, outline='#447add', width=2)
    draw.rounded_rectangle([(60, 160), (460, 225)], radius=15, outline='#447add', width=2)
    draw.rounded_rectangle([(580, 160), (970, 225)], radius=15, outline='#447add', width=2)

    # Credit
    draw.text((350, 695), "CREATED BY: ", font=ImageFont.truetype(SKYFONT, 14), fill="white")
    draw.text((470, 695), "AMIR AMEMI", font=ImageFont.truetype(SKYFONT, 14), fill="#447add")

    # Save report
    report_img.save(output_path)
    print(f"✅ Report saved as {output_path}")
    return output_path, worst_flight