import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Path to your CSV file
csv_file_path = 'daily_tweet_stats.csv'

# Read the CSV file into a pandas DataFrame
try:
    df = pd.read_csv(csv_file_path, parse_dates=['date'])
except FileNotFoundError:
    print(f"Error: The file '{csv_file_path}' was not found.")
    exit()
except pd.errors.ParserError:
    print(f"Error: Could not parse the file '{csv_file_path}'. Please check the file format.")
    exit()

# Check if necessary columns exist
required_columns = {'date', 'tweet_count', 'retweet_count'}
if not required_columns.issubset(df.columns):
    print(f"Error: The CSV file must contain the columns: {required_columns}")
    exit()

# Calculate the total activity per day
df['total_activity'] = df['tweet_count'] + df['retweet_count']

# Sort the DataFrame by date (if not already sorted)
df = df.sort_values('date')

# Set the figure size
plt.figure(figsize=(12, 6))

# Plot the total activity
plt.plot(df['date'], df['total_activity'], marker='o', linestyle='-', color='blue', label='Total Activity')

# Formatting the x-axis to show dates properly
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Major ticks every month
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format as 'YYYY-MM'

plt.xlabel('Date')
plt.ylabel('Number of Tweets and Retweets')
plt.title('Daily Total Tweets and Retweets')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Save the plot as a PNG file (optional)
plt.savefig('daily_total_tweets_retweets.png')

# Display the plot
plt.show()
