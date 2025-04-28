import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib import font_manager as fm


# ========================
# Delay Statistics
# ========================
def compute_delays(df):
    """
    Calculate sum, max, average, and min for departure and arrival delays.

    Args:
        df (pd.DataFrame): Flight data

    Returns:
        tuple: (sum_dep, max_dep, avg_dep, min_dep, sum_arr, max_arr, avg_arr, min_arr)
    """
    return (
        df['departure_delay'].sum(),
        df['departure_delay'].max(),
        df['departure_delay'].mean(),
        df['departure_delay'].min(),
        df['arrival_delay'].sum(),
        df['arrival_delay'].max(),
        df['arrival_delay'].mean(),
        df['arrival_delay'].min(),
    )


# ========================
# Flight Status Counts
# ========================
def compute_status(df):
    """
    Count number of flights per status.

    Args:
        df (pd.DataFrame): Flight data

    Returns:
        tuple: (active, scheduled, landed, cancelled)
    """
    return (
        df[df['flight_status'] == 'active'].count(),
        df[df['flight_status'] == 'scheduled'].count(),
        df[df['flight_status'] == 'landed'].count(),
        df[df['flight_status'] == 'cancelled'].count(),
    )


def flight_status_distribution(df):
    """
    Alternative method to get number of flights by status.

    Args:
        df (pd.DataFrame): Flight data

    Returns:
        tuple: (cancelled, active, landed, scheduled)
    """
    return (
        (df['flight_status'] == 'cancelled').sum(),
        (df['flight_status'] == 'active').sum(),
        (df['flight_status'] == 'landed').sum(),
        (df['flight_status'] == 'scheduled').sum(),
    )


# ========================
# Top Delayed Routes
# ========================
def top_delayed_routes(df, top_n=5):
    """
    Find the top N most delayed routes by average departure delay.

    Args:
        df (pd.DataFrame): Flight data
        top_n (int): Number of routes to return

    Returns:
        pd.Series: Delayed routes and average delay
    """
    return (
        df.groupby(['departure_iata', 'arrival_iata'])['departure_delay']
          .mean()
          .sort_values(ascending=False)
          .head(top_n)
          .astype(int)
    )


# ========================
# Font and Plot Styling
# ========================
def get_font_prop(font_name: str, size_font: int):
    """
    Load a custom font for plots.

    Args:
        font_name (str): Font path
        size_font (int): Font size

    Returns:
        FontProperties: Loaded font object
    """
    return fm.FontProperties(fname=font_name, size=size_font)


def ax_metadata(ax, title: str, font_prop):
    """
    Style plot axes with black background and white texts.

    Args:
        ax (matplotlib.axes._axes.Axes): Axis to style
        title (str): Plot title
        font_prop: Font properties object
    """
    ax.set_facecolor("black")
    ax.set_title(title, fontproperties=font_prop, y=1.3, fontsize=9, color="white")
    ax.set_xlabel(None)
    ax.set_ylabel("Minutes")
    ax.spines["bottom"].set_color("white")
    ax.spines["left"].set_color("white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.tick_params(axis="y", colors="white")
    ax.tick_params(axis="x", colors="white")


# ========================
# Plot Functions
# ========================
def plot_hourly_avg_delays(df, font_path, output_path):
    """
    Plot hourly average departure and arrival delays.

    Args:
        df (pd.DataFrame): Average delay data
        font_path (str): Font path
        output_path (str): Output file path to save
    """
    font_prop = get_font_prop(font_path, 7)
    fig, ax = plt.subplots(facecolor="black", figsize=(9, 2))

    df_sorted = df.sort_values(by='hour')
    ax.set_xticks(df_sorted['hour'].unique())
    ax.set_xticklabels(df_sorted['hour'].unique())

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
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)


def plot_top_delayed_routes(result, font_path, output_path):
    """
    Plot the top delayed routes as a bar chart.

    Args:
        result (pd.Series): Delayed routes data
        font_path (str): Font path
        output_path (str): Output file path to save
    """
    font_prop = get_font_prop(font_path, 6)
    fig, ax = plt.subplots(facecolor="black", figsize=(9, 2))

    routes = [f"{dep} → {arr}" for dep, arr in result.index]
    ax.bar(routes, result.values, width=0.2, color='#4175d4')
    ax.set_xticklabels(routes, ha='center')

    ax.set_ylabel("Average Departure Delay (minutes)", fontsize=9, color="white")
    ax_metadata(ax, "Top 10 Most Delayed Routes", font_prop)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)
