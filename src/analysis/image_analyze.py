import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from src.analysis.analyze_delays import plot_hourly_avg_delays,plot_top_delayed_routes

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

def add_banner(report, x, y, label: str, value):
    """
    Function to create the label and it's value
    the label will be in orange
    the value will be in white
    Args:
        report (ImageDraw): the report image pillow
        x (_type_): the x position
        y (_type_): the y position
        label (str): the label string will be in orange
        value (_type_): the value of the label will be in white

    :returns:
        _type_: the image updated with the new Banner LABEL : VALUE
    """

    report.text(
        (x + 10, y),
        label,
        font=ImageFont.truetype(SKYFONT_INVERTED, FONT_SIZE),
        fill="black",
    )
    width_text, height_text = get_text_dimensions(
        label, ImageFont.truetype(SKYFONT_INVERTED, FONT_SIZE)
    )
    report.text(
        (x + width_text + 10, y),
        str(value),
        font=ImageFont.truetype(SKYFONT, FONT_SIZE),
        fill="white",
    )
    report.text(
        (x + 10, y),
        label,
        font=ImageFont.truetype(SKYFONT, FONT_SIZE),
        fill="orange",
    )

    return get_text_dimensions(
        f"{label} {value}", ImageFont.truetype(SKYFONT, FONT_SIZE)
    )

def generate_report_image(df,df_st,top_delay_path,hourly_delay_path, output_path="final_report.png"):
    # Create the main white background
    report_img = Image.new("RGB", (1080, 720), color="white")
    draw = ImageDraw.Draw(report_img)
    font = ImageFont.truetype("arial.ttf", size=20)

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



    # Write KPIs
    # kpi_texts = [
    #     f"Scheduled: {scheduled}",
    #     f"Cancelled: {canceled}",
    #     f"Active: {active}",
    #     f"Landed: {landed}"
    # ]
    kpi_texts = [
        f"NOUVLAIR FLIGHTS       SCHEDULED: {scheduled}      CANCELLED: {canceled}      ACTIVE: {active}      LANDED: {landed}"
    ]
    stats_dep_text = [f"  DELAYED DEPARTURE: {dep_stats[3]}",
                      f"MIN: {dep_stats[0]}   MAX: {dep_stats[1]}   AVG: {dep_stats[2]}"]
    stats_arr_text = [f"  DELAYED ARRIVAL: {arr_stats[3]}",
                      f"MIN: {arr_stats[0]}   MAX: {arr_stats[1]}   AVG: {arr_stats[2]}"]

    for idx, text in enumerate(kpi_texts):
        draw.text((50, 50 + idx * 30), text, font=font, fill="white")

    for idx, text in enumerate(stats_dep_text):
        draw.text((50, 100 + idx * 30), text, font=font, fill="white")
    
    for idx, text in enumerate(stats_arr_text):
        draw.text((600, 100 + idx * 30), text, font=font, fill="white")

    # Find worst flight (highest arrival delay)
    worst_flight = df.loc[df['arrival_delay'].idxmax()]
    worst_flight_text = (f"Worst Flight: {worst_flight['airline_name']} {worst_flight['flight_iata']} "
                         f"from {worst_flight['departure_airport']} to {worst_flight['arrival_airport']} "
                         f"Delay: {worst_flight['arrival_delay']} min")
    draw.text((50, 200), worst_flight_text, font=font, fill="red")

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

    report_img.paste(hourly_delay, (-30, 300))
    report_img.paste(top_delay, (50, 500))

    report_img.save(output_path)
    print(f"Report saved as {output_path}")

# Example usage:
# df = pd.read_csv("your_clean_dataframe.csv")
# generate_report_image(df)
