import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive Agg backend, otherwise causes error for MacOS
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_activity_window(count_all, count_tweets, center_date_str, window_days, csv_file_path='daily_tweet_stats.csv', save_plot=False, output_file='activity_window_plot.png'):

    # 1. Parse the center date using pandas
    try:
        center_date = pd.to_datetime(center_date_str, format='%m/%d/%Y')
    except ValueError:
        print(f"Error: The date '{center_date_str}' is not in the expected 'MM/DD/YYYY' format.")
        return

    # 2. Calculate the start and end dates
    start_date = center_date - pd.Timedelta(days=window_days)
    end_date = center_date + pd.Timedelta(days=window_days)

    # 3. Read the CSV file
    try:
        df = pd.read_csv(csv_file_path, parse_dates=['date'])
    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found.")
        return
    except pd.errors.ParserError:
        print(f"Error: Could not parse the file '{csv_file_path}'. Please check the file format.")
        return

    # # 4. Validate required columns
    # required_columns = {'date', 'tweet_count', 'retweet_count'}
    # if not required_columns.issubset(df.columns):
    #     print(f"Error: The CSV file must contain the columns: {required_columns}")
    #     return

    # 5. Calculate activities
    if count_all:
        df['total_activity'] = df['tweet_count'] + df['retweet_count']
    else:
        if count_tweets:
            df['total_activity'] = df['tweet_count']
        else:
            df['total_activity'] = df['retweet_count']

    # 6. Filter the DataFrame for the specified window
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    window_df = df.loc[mask].copy()

    if window_df.empty:
        print(f"No data available for the specified date range: {start_date.date()} to {end_date.date()}.")
        return

    # 7. Sort the DataFrame by date
    window_df = window_df.sort_values('date')

    # 8. Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(window_df['date'], window_df['total_activity'], marker='o', linestyle='-', color='blue', label='Total Activity')

    # Optional: Plot tweet_count and retweet_count separately
    # plt.plot(window_df['date'], window_df['tweet_count'], marker='o', linestyle='-', color='green', label='Tweet Count')
    # plt.plot(window_df['date'], window_df['retweet_count'], marker='o', linestyle='-', color='red', label='Retweet Count')

    # Formatting the x-axis
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))  # Major ticks every week
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format as 'YYYY-MM-DD'

    plt.xlabel('Date')
    plt.ylabel('Number of Tweets and Retweets')
    plt.title(f'Daily Total Tweets and Retweets\nCenter Date: {center_date.strftime("%m/%d/%Y")} ±{window_days} Days')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Save the plot if requested
    if save_plot:
        # Format the center date to 'MM-DD-YYYY' for the filename
        safe_center_date_str = center_date.strftime('%m-%d-%Y')  # Format: 'MM-DD-YYYY'
        # Update the output_file with the formatted date
        if count_all:
            output_file = f'all_activity_window_around_{safe_center_date_str}.png'
        else:
            if count_tweets:
                output_file = f'tweets_activity_window_around_{safe_center_date_str}.png'
            else:
                output_file = f'retweets_activity_window_around_{safe_center_date_str}.png'
        plt.savefig(output_file)
        print(f"Plot has been saved as '{output_file}'.")

    # Display the plot (commented out to prevent hanging)
    # plt.show()

# Example Usage
if __name__ == "__main__":
    # Define the center date and window
    center_date_input = '3/31/2024'  # Format: 'MM/DD/YYYY'
    window_days_input = 45  # Number of days before and after the center date
    count_all = False
    count_tweets = True
    # Call the function to plot the activity window
    plot_activity_window(
        count_all,
        count_tweets, 
        center_date_str=center_date_input,
        window_days=window_days_input,
        save_plot=True,  # Set to True to save the plot as an image file
        output_file=f'activity_window_around_{center_date_input}.png'  # overrides if already exists
    )
