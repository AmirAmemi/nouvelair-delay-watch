import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

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
    # print(f"Average Departure Delay: {avg_dep_delay:.2f} mins")
    # print(f"Average Arrival Delay: {avg_arr_delay:.2f} mins")
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
    # cancelled_count = (df['flight_status'].str.lower() == 'cancelled').sum() if 'cancelled' in df['flight_status'].str.lower() else 0
    # active_count    = (df['flight_status'].str.lower() == 'active').sum() if 'active' in df['flight_status'].str.lower() else 0
    # landed_count    = (df['flight_status'].str.lower() == 'landed').sum() if 'landed' in df['flight_status'].str.lower() else 0
    # scheduled_count = (df['flight_status'].str.lower() == 'scheduled').sum() if 'scheduled' in df['flight_status'].str.lower() else 0
    return cancelled_count,active_count,landed_count,scheduled_count


# ---- Top Delayed Routes ----
def top_delayed_routes(df, top_n=5):
    return df.groupby(['departure_airport', 'arrival_airport'])['departure_delay'].mean() \
             .sort_values(ascending=False).head(top_n)

# ---- Visualization ----
def plot_delay_trend(df):
    daily_delay = df.groupby(df['flight_date'].dt.date)['departure_delay'].mean()
    plt.figure(figsize=(10,5))
    daily_delay.plot(kind='line', marker='o')
    plt.title("Daily Average Departure Delay")
    plt.xlabel("Date")
    plt.ylabel("Average Delay (min)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('dashboard/daily_delay_trend.png')
    plt.close()

def plot_status_distribution(df):
    status_counts = df['flight_status'].value_counts()
    plt.figure(figsize=(6,6))
    status_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title("Flight Status Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig('dashboard/status_distribution.png')
    plt.close()

# ---- Run all ----
# if __name__ == "__main__":
    # # compute_average_delays(df)
    # print(flight_status_distribution(df))
    # print(top_delayed_routes(df))
    # plot_delay_trend(df)
    # plot_status_distribution(df)
