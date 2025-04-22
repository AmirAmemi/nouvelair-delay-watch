import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load cleaned data
df = pd.read_csv(f'data/cleaned_flights_{datetime.today().strftime("%Y-%m-%d")}.csv')

# Convert to datetime if not already
df['departure.estimated'] = pd.to_datetime(df['departure.estimated'])
df['arrival.estimated'] = pd.to_datetime(df['arrival.estimated'])
df['flight_date'] = pd.to_datetime(df['flight_date'])

# ---- Delay Statistics ----
def compute_average_delays(df):
    avg_dep_delay = df['departure.delay'].mean()
    avg_arr_delay = df['arrival.delay'].mean()
    print(f"Average Departure Delay: {avg_dep_delay:.2f} mins")
    print(f"Average Arrival Delay: {avg_arr_delay:.2f} mins")
    return avg_dep_delay, avg_arr_delay

# ---- Status Breakdown ----
def flight_status_distribution(df):
    return df['flight_status'].value_counts()

# ---- Top Delayed Routes ----
def top_delayed_routes(df, top_n=5):
    return df.groupby(['departure.airport', 'arrival.airport'])['departure.delay'].mean() \
             .sort_values(ascending=False).head(top_n)

# ---- Visualization ----
def plot_delay_trend(df):
    daily_delay = df.groupby(df['flight_date'].dt.date)['departure.delay'].mean()
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
if __name__ == "__main__":
    compute_average_delays(df)
    print(flight_status_distribution(df))
    print(top_delayed_routes(df))
    plot_delay_trend(df)
    plot_status_distribution(df)
