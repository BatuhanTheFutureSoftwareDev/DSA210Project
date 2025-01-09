import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive Agg backend, otherwise causes error for MacOS
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_activity_window(center_date_str, window_days, csv_file_path='daily_tweet_stats.csv', save_plot=False, output_file='activity_window_plot.png'):
    try:
        center_date = pd.to_datetime(center_date_str, format='%m/%d/%Y')
    except ValueError:
        print(f"Error: The date '{center_date_str}' is not in the expected 'MM/DD/YYYY' format.")
        return

    start_date = center_date - pd.Timedelta(days=window_days)
    end_date = center_date + pd.Timedelta(days=window_days)

    try:
        df = pd.read_csv(csv_file_path, parse_dates=['date'])
    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found.")
        return
    except pd.errors.ParserError:
        print(f"Error: Could not parse the file '{csv_file_path}'. Please check the file format.")
        return

    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    window_df = df.loc[mask].copy()

    if window_df.empty:
        print(f"No data available for the specified date range: {start_date.date()} to {end_date.date()}.")
        return

    window_df = window_df.sort_values('date')

    plt.figure(figsize=(14, 7))
    plt.plot(window_df['date'], window_df['total_activity'], marker='o', linestyle='-', color='blue', label='Total Activity')

    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))  # Major ticks every week
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format as 'YYYY-MM-DD'

    plt.xlabel('Date')
    plt.ylabel('Number of Tweets and Retweets')
    plt.title(f'Daily Total Tweets and Retweets\nCenter Date: {center_date.strftime("%m/%d/%Y")} ±{window_days} Days')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.xticks(rotation=45)

    if save_plot: # optional
        safe_center_date_str = center_date.strftime('%m-%d-%Y')  # Format: 'MM-DD-YYYY'
        output_file = f'all_activity_window_around_{safe_center_date_str}.png'
        plt.savefig(output_file)
        print(f"Plot has been saved as '{output_file}'.")

if __name__ == "__main__": # A demonstration
    # Define the center date and window
    center_date_input = '5/14/2023'  # Format: 'MM/DD/YYYY'
    window_days_input = 30  # Number of days before and after the center date

    plot_activity_window(
        center_date_str=center_date_input,
        window_days=window_days_input,
        save_plot=True,
        output_file=f'activity_window_around_{center_date_input}.png'  # Overrides if already exists
    )
