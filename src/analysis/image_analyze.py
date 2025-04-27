import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
# from src.analysis.analyze_delays import plot_hourly_avg_delays,plot_top_delayed_routes
# from main import SKYFONT,SKYFONT_INVERTED,GLYPH_AIRPORT
# Assume you have a DataFrame ready, called df
# Columns assumed: ['departure_delay', 'arrival_delay', 'flight_status', 'departure_airport', 'arrival_airport', 'flight_number', 'airline']

def create_simple_plot(values, labels, title, ylabel, output_path):
    plt.figure(figsize=(5, 3))
    plt.bar(labels, values, color='orange')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def get_text_dimensions(text_string: str, font):
    """
    will return the dimensions in pixels of the text
    Args:
        text_string (str): the text string that will be outputted
        font (ImageFont): the font used for the text

    :returns:
        _type_: text_width and text_height
    """
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)
def past_titles(report,SKYFONT, datetime_query):
    """
    To generate titles in the white AREA
    Args:
        report (_type_): the report from PILLOW
        datetime_query (_type_): query date formatted DD/MM/YYYY
    """
    # Last update hour
    report.text(
        (55, 60),
        f"LAST UPDATE AT {datetime_query.strftime('%#H:%M')}",
        font=ImageFont.truetype(SKYFONT, 9),
        fill="black",
    )
    # Big Title
    report.text(
        (260, 10),
        f"NOUVELAIR DAILY INGEST {datetime_query.strftime('%a %d %B %Y').upper()}",
        font=ImageFont.truetype(SKYFONT, 25),
        fill="black",
    )
    # Subtitle
    report.text(
        (260, 50),
        "NOUVELAIR FLIGHT DELAY ANALYSIS REPORT",
        font=ImageFont.truetype(SKYFONT, 15),
        fill="black",
    )
    return report

def generate_report_image(df,df_st,top_delay_path,hourly_delay_path, SKYFONT, output_path="final_report.png"):
    # Create the main white background
    report_img = Image.new("RGB", (1080, 720), color="black")





    # LOGO BLOCK
    logo_path = "src/analysis/nouvelair_logo.png"
    # logo = Image.open(logo_path)
    # draw.paste(logo,(25,7))
    if os.path.exists(logo_path):
        with Image.open(logo_path) as nouvelair_logo:
            # Do something with the image
            report_img.paste(nouvelair_logo, (0, 0))
            # TITLES BLOCKS
            draw = ImageDraw.Draw(report_img)
            date_now = datetime.now()
            past_titles(draw,SKYFONT,date_now) 
    else:
        print(f"Logo not found at {logo_path}")
    # with Image.open("nouvelair_logo.png") as nouvelair_logo:
    #     draw.paste(nouvelair_logo, (25, 7))





    # draw = ImageDraw.Draw(report_img)
    # font = ImageFont.truetype("arial.ttf", size=20)
    font = ImageFont.truetype(SKYFONT, size=17)


    

    


    # KPIs
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


    # Write KPIs
    # kpi_texts = [
    #     f"Scheduled: {scheduled}",
    #     f"Cancelled: {canceled}",
    #     f"Active: {active}",
    #     f"Landed: {landed}"
    # ]
    kpi_texts = [
        f"NOUVLAIR FLIGHTS       SCHEDULED: {scheduled}     CANCELLED: {canceled}     ACTIVE: {active}     LANDED: {landed}"
    ]
    stats_dep_text = [f"  DELAYED DEPARTURE: {int(dep_stats[3]/60)}H",
                      f"MIN: {dep_stats[0]}M   MAX: {dep_stats[1]}M   AVG: {dep_stats[2]}M"]
    stats_arr_text = [f"  DELAYED ARRIVAL: {int(arr_stats[3]/60)}H",
                      f"MIN: {arr_stats[0]}M   MAX: {arr_stats[1]}M   AVG: {arr_stats[2]}M"]

    
    worst_flight_text = [f"WORST FLIGHT:",f"{worst_flight['airline_name']} {worst_flight['flight_iata']} ",
                         f" { worst_flight['departure_airport']} -----   DELAY OF {int(worst_flight['arrival_delay']+ worst_flight['departure_delay'])} MIN   -----> {worst_flight['arrival_airport']} "]
    
    for idx, text in enumerate(kpi_texts):
        draw.text((30, 120 + idx * 30), text, font=ImageFont.truetype(SKYFONT, size=15), fill="white")

    for idx, text in enumerate(stats_dep_text):
        draw.text((80, 170 + idx * 30), text, font=ImageFont.truetype(SKYFONT, size=15), fill="white")
    
    for idx, text in enumerate(stats_arr_text):
        draw.text((600, 170 + idx * 30), text, font=ImageFont.truetype(SKYFONT, size=15), fill="white")

    draw.text((300,235),worst_flight_text[0],font=ImageFont.truetype(SKYFONT, size=14),fill="#447add")
    draw.text((480,235),worst_flight_text[1],font=ImageFont.truetype(SKYFONT, size=14),fill="white")
    draw.text((270,265),worst_flight_text[2],font=ImageFont.truetype(SKYFONT, size=14),fill="white")

    

    # for idx, text in enumerate(worst_flight_text):
    #     # draw.text((50, 50 ), text, font=font, fill="white")
    #     draw.text((300, 200 + idx * 30), text, font=font, fill="red")

    # Find worst flight (highest arrival delay)

    worst_flight = df.loc[df['arrival_delay'].idxmax()]
    worst_flight_text = (f"Worst Flight: {worst_flight['airline_name']} {worst_flight['flight_iata']} "
                         f"from {worst_flight['departure_airport']} to {worst_flight['arrival_airport']} "
                         f"Delay: {worst_flight['arrival_delay']} min")

    # # First line text parts
    # label_text = "WORST FLIGHT: "
    # flight_text = f"{worst_flight['airline_name']} {worst_flight['flight_iata']}"

    # # Second line text
    # departure = worst_flight['departure_airport']
    # arrival = worst_flight['arrival_airport']
    # delay = worst_flight['arrival_delay']
    # second_line_text = f"✈️  {departure} ----DELAY OF {int(delay)}M----> {arrival} ✈️"

    # # Coordinates
    # x_first_line = 400  # Adjust this if needed
    # y_first_line = 50

    # x_second_line = 250  # Adjust to center it nicely
    # y_second_line = 150

    # # Draw first line
    # draw.text((x_first_line, y_first_line), label_text, font=font, fill="#447add")
    # label_width = draw.textlength(label_text, font=font)
    # draw.text((x_first_line + label_width, y_first_line), flight_text, font=font, fill="white")

    # # Draw second line
    # draw.text((x_second_line, y_second_line), second_line_text, font=font, fill="white")


    # top_left = (30, 290)  # Top-left corner
    # bottom_right = (1000, 710)  # Bottom-right corner
    # radius = 30  # Radius for the rounded corners
    # border_color = '#447add' # Border color (black)
    # border_thickness = 1.5  # Border thickness

    # Draw the rounded rectangle with empty center (only the border is filled)
    
    # draw.rounded_rectangle([(30,290), (1000, 710)], radius=30, outline='#447add', width=1.5)

    
    
    
    # draw.text(
    #     (x + width_text + 10, y),
    #     str(value),
    #     font=ImageFont.truetype(SKYFONT, FONT_SIZE),
    #     fill="white",
    # )
    # report.text(
    #     (x + 10, y),
    #     label,
    #     font=ImageFont.truetype(SKYFONT_INVERTED, FONT_SIZE),
    #     fill="black",
    # )
    # width_text, height_text = get_text_dimensions(
    #     label, ImageFont.truetype(SKYFONT_INVERTED, FONT_SIZE)
    # )
    # report.text(
    #     (x + width_text + 10, y),
    #     str(value),
    #     font=ImageFont.truetype(SKYFONT, FONT_SIZE),
    #     fill="white",
    # )
    # report.text(
    #     (x + 10, y),
    #     label,
    #     font=ImageFont.truetype(SKYFONT, FONT_SIZE),
    #     fill="orange",
    # )

    # return get_text_dimensions(
    #     f"{label} {value}", ImageFont.truetype(SKYFONT, FONT_SIZE)
    # )

    # Delay stats
    # dep_delays = df['departure_delay'].dropna()
    # arr_delays = df['arrival_delay'].dropna()

    # dep_stats = [dep_delays.min(), dep_delays.max(), dep_delays.mean(), dep_delays.sum()]
    # arr_stats = [arr_delays.min(), arr_delays.max(), arr_delays.mean(), arr_delays.sum()]
    # top_delay_path = "top_delay_plot.png"
    # hourly_delay_path = "hourly_delay_plot.png"
    # plot_top_delayed_routes(df,10,top_delay_path)
    # plot_hourly_avg_delays(df_avg_data,plot_font,hourly_delay_path)
    # Create and paste plots
    # create_simple_plot(dep_stats, ["Min", "Max", "Avg", "Sum"], "Departure Delays", "Minutes", "dep_delay_plot.png")
    # create_simple_plot(arr_stats, ["Min", "Max", "Avg", "Sum"], "Arrival Delays", "Minutes", "arr_delay_plot.png")

    top_delay = Image.open(top_delay_path)
    hourly_delay = Image.open(hourly_delay_path)

    report_img.paste(hourly_delay, (50, 290))
    report_img.paste(top_delay, (50, 490))

    draw.rounded_rectangle([(30, 310), (1000, 680)], radius=15, outline='#447add', width=2)
    draw.rounded_rectangle([(60, 160), (460, 225)], radius=15, outline='#447add', width=2)
    draw.rounded_rectangle([(580, 160), (970, 225)], radius=15, outline='#447add', width=2)

    draw.text((350,695),"MADE BY: ",font=ImageFont.truetype(SKYFONT, size=14),fill="white")
    draw.text((470,695),"AMIR AMEMI ",font=ImageFont.truetype(SKYFONT, size=14),fill="#447add")
    report_img.save(output_path)
    print(f"Report saved as {output_path}")

# Example usage:
# df = pd.read_csv("your_clean_dataframe.csv")
# generate_report_image(df)
