import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

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

def generate_report_image(df,df_st, output_path="final_report.png"):
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

    # Write KPIs
    kpi_texts = [
        f"Scheduled: {scheduled}",
        f"Cancelled: {canceled}",
        f"Active: {active}",
        f"Landed: {landed}"
    ]

    for idx, text in enumerate(kpi_texts):
        draw.text((50, 50 + idx * 30), text, font=font, fill="black")

    # Find worst flight (highest arrival delay)
    worst_flight = df.loc[df['arrival_delay'].idxmax()]
    worst_flight_text = (f"Worst Flight: {worst_flight['airline_name']} {worst_flight['flight_iata']} "
                         f"from {worst_flight['departure_airport']} to {worst_flight['arrival_airport']} "
                         f"Delay: {worst_flight['arrival_delay']} min")
    draw.text((50, 200), worst_flight_text, font=font, fill="red")

    # Delay stats
    dep_delays = df['departure_delay'].dropna()
    arr_delays = df['arrival_delay'].dropna()

    dep_stats = [dep_delays.min(), dep_delays.max(), dep_delays.mean(), dep_delays.sum()]
    arr_stats = [arr_delays.min(), arr_delays.max(), arr_delays.mean(), arr_delays.sum()]

    # Create and paste plots
    create_simple_plot(dep_stats, ["Min", "Max", "Avg", "Sum"], "Departure Delays", "Minutes", "dep_delay_plot.png")
    create_simple_plot(arr_stats, ["Min", "Max", "Avg", "Sum"], "Arrival Delays", "Minutes", "arr_delay_plot.png")

    dep_plot = Image.open("dep_delay_plot.png")
    arr_plot = Image.open("arr_delay_plot.png")

    report_img.paste(dep_plot, (50, 300))
    report_img.paste(arr_plot, (550, 300))

    report_img.save(output_path)
    print(f"Report saved as {output_path}")

# Example usage:
# df = pd.read_csv("your_clean_dataframe.csv")
# generate_report_image(df)
