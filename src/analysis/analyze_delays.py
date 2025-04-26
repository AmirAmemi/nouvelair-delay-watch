import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib import font_manager as fm

# Load cleaned data
# df = pd.read_csv(f'data/cleaned_flights_2025-04-22.csv')

# # Convert to datetime if not already
# df['departure_estimated'] = pd.to_datetime(df['departure_estimated'])
# df['arrival_estimated'] = pd.to_datetime(df['arrival_estimated'])
# df['flight_date'] = pd.to_datetime(df['flight_date'])

# ---- Delay Statistics ----
def compute_delays(df):
    sum_dep_delay = df['departure_delay'].sum()
    max_dep_delay = df['departure_delay'].max()
    avg_dep_delay = df['departure_delay'].mean()
    min_dep_delay = df['departure_delay'].min()
    sum_arr_delay = df['arrival_delay'].sum()
    max_arr_delay = df['arrival_delay'].max()
    avg_arr_delay = df['arrival_delay'].mean()
    min_arr_delay = df['arrival_delay'].min()
    return sum_dep_delay,max_dep_delay,avg_dep_delay,min_dep_delay,sum_arr_delay,max_arr_delay, avg_arr_delay,min_arr_delay

def compute_status(df):
    sum_schedule = df[df['flight_status'] == 'scheduled'].count()
    sum_active = df[df['flight_status'] == 'active'].count()
    sum_landed = df[df['flight_status'] == 'landed'].count()
    sum_cancelled = df[df['flight_status'] == 'cancelled'].count()
    return sum_active,sum_schedule,sum_landed,sum_cancelled

# ---- Status Breakdown ----
def flight_status_distribution(df):
    cancelled_count = (df['flight_status'] == 'cancelled').sum() 
    active_count    = (df['flight_status'] == 'active').sum() 
    landed_count    = (df['flight_status'] == 'landed').sum() 
    scheduled_count = (df['flight_status'] == 'scheduled').sum() 
    return cancelled_count,active_count,landed_count,scheduled_count


# ---- Top Delayed Routes ----
def top_delayed_routes(df, top_n=5):
    return df.groupby(['departure_iata', 'arrival_iata'])['departure_delay'].mean() \
             .sort_values(ascending=False).head(top_n).astype({'departure_delay':int})

# ---- Visualization ----



# def plot_top_delayed_routes(result):
#     """
#     Plots top delayed routes from result of top_delayed_routes function.
    
#     Parameters:
#     result (pd.Series): Output from top_delayed_routes(df), indexed by (departure_airport, arrival_airport)
#     """
#     # Extract route names from index
#     routes = [f"{dep} → {arr}" for dep, arr in result.index]
    
#     # Plot setup
#     plt.figure(figsize=(10, 6))
#     # plt.style.use('white')

    
#     # Bar plot (vertical)
#     plt.bar(routes, result.values, color='yellow')
#     plt.xticks(rotation=45, ha='right')
#     plt.ylabel('Average Departure Delay (minutes)', fontsize=12)
#     plt.title('Top Most Delayed Routes', fontsize=16)
#     # plt.grid(axis='y', linestyle='--', alpha=0.5)
#     plt.tight_layout()

#     # Show plot
#     plt.show()
# def plot_hourly_avg_delays(df):
#     """
#     Plots average hourly delays for departure and arrival.
    
#     Parameters:
#     df (pd.DataFrame): Must include 'hour', 'avg_departure_delay', 'avg_arrival_delay' columns.
#     """
#     # Ensure hour is sorted
#     df = df.sort_values(by='hour')
    
#     # Plot setup
#     plt.figure(figsize=(12, 6))
#     plt.style.use('dark_background')

#     # Plot departure and arrival delay
#     plt.plot(df['hour'], df['avg_departure_delay'], color='yellow', marker='o', label='Avg Departure Delay')
#     plt.plot(df['hour'], df['avg_arrival_delay'], color='white', marker='o', label='Avg Arrival Delay')

#     # Labels and titles
#     plt.title('Hourly Average Delays', fontsize=16)
#     plt.xlabel('Hour of Day', fontsize=12)
#     plt.ylabel('Average Delay (minutes)', fontsize=12)
#     plt.xticks(range(0, 24))  # Ensure all hours show
#     # plt.grid(False, linestyle='', alpha=0.5)
#     plt.legend()
#     plt.tight_layout()

#     # Show plot
#     plt.show()


def get_font_prop(font_name: str, size_font: int):
    return fm.FontProperties(fname=font_name, size=size_font)


def ax_metadata(ax, title: str, font_prop,):
    ax.set_facecolor("black")
    ax.set_title(title, fontproperties=font_prop, y=1.2, fontsize=12, color="white")
    ax.set_xlabel(None)
    ax.set_ylabel("Minutes")
    ax.spines["bottom"].set_color("white")
    ax.spines["left"].set_color("white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.tick_params(axis="y", colors="white")
    ax.tick_params(axis="x", colors="white")


def plot_hourly_avg_delays(df, font_path,output_path):
# def plot_hourly_avg_delays(df, font_path):
    font_prop = get_font_prop(font_path, 10)
    fig, ax = plt.subplots(facecolor="black", figsize=(12, 2))

    df_sorted = df.sort_values(by='hour')
    
    ax.set_xticks(df['hour'].unique())
    ax.set_xticklabels(df['hour'].unique())
    df_sorted.plot(
        x='hour',
        y=['avg_departure_delay', 'avg_arrival_delay'],
        kind='line',
        ax=ax,
        marker='x',
        color={
            'avg_departure_delay': '#4175d4',
            'avg_arrival_delay': 'white'
        }
    )

    ax_metadata(ax, "Average Hourly Delays", font_prop)
    ax.legend(facecolor="black", labelcolor="white", prop=font_prop)
    plt.savefig(output_path)
    # plt.show()


# def plot_top_delayed_routes(result, font_path):
def plot_top_delayed_routes(result, font_path,output_path):
    font_prop = get_font_prop(font_path, 10)
    fig, ax = plt.subplots(facecolor="black", figsize=(10, 2))

    routes = [f"{dep} → {arr}" for dep, arr in result.index]
    ax.bar(routes, result.values,width = 0.2, color='#4175d4')
    ax.set_xticklabels(routes, ha='center')

    ax.set_ylabel("Average Departure Delay (minutes)", fontsize=12, color="white")
    ax_metadata(ax, "Top 10 Most Delayed Routes", font_prop)
    plt.tight_layout()
    plt.savefig(output_path)
    # plt.show()

# ---- Run all ----
# if __name__ == "__main__":
    # # compute_average_delays(df)
    # print(flight_status_distribution(df))
    # print(top_delayed_routes(df))
    # plot_delay_trend(df)
    # plot_status_distribution(df)
