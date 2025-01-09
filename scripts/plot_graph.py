import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

csv_file_path = 'daily_tweet_stats.csv'

try:
    df = pd.read_csv(csv_file_path, parse_dates=['date'])
except FileNotFoundError:
    print(f"Error: The file '{csv_file_path}' was not found.")
    exit()
except pd.errors.ParserError:
    print(f"Error: Could not parse the file '{csv_file_path}'. Please check the file format.")
    exit()

required_columns = {'date', 'tweet_count', 'retweet_count'}
if not required_columns.issubset(df.columns):
    print(f"Error: The CSV file must contain the columns: {required_columns}")
    exit()

df['total_activity'] = df['tweet_count'] + df['retweet_count']

df = df.sort_values('date')

plt.figure(figsize=(12, 6))

plt.plot(df['date'], df['total_activity'], marker='o', linestyle='-', color='blue', label='Total Activity')

plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.xlabel('Date')
plt.ylabel('Number of Tweets and Retweets')
plt.title('Daily Total Tweets and Retweets')
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.xticks(rotation=45)

plt.savefig('daily_total_tweets_retweets.png')

plt.show()
