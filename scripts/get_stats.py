import json
import pandas as pd
from bs4 import BeautifulSoup

def extract_json_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.find('script', type='application/json')
    if script_tag:
        return json.loads(script_tag.string)
    else:
        raise ValueError("No JSON script tag found in the HTML.")

json_file_path = 'my_tweets.json'

with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

tweets_data = []

for entry in data:
    tweet = entry.get('tweet', {})
    
    created_at_str = tweet.get('created_at', '')
    if not created_at_str:
        continue 
    
    try:
        created_at = pd.to_datetime(created_at_str)
        tweet_date = created_at.date()
    except Exception as e:
        print(f"Error parsing date '{created_at_str}': {e}")
        continue
    
    full_text = tweet.get('full_text', '')
    is_retweet = 1 if full_text.startswith('RT @') else 0
    
    tweets_data.append({
        'date': tweet_date,
        'is_retweet': is_retweet
    })

df = pd.DataFrame(tweets_data)
tweet_counts = df.groupby('date').size().reset_index(name='tweet_count')
retweet_counts = df.groupby('date')['is_retweet'].sum().reset_index(name='retweet_count')
daily_stats = pd.merge(tweet_counts, retweet_counts, on='date')
daily_stats = daily_stats.sort_values('date')

date_range = pd.date_range(start=daily_stats['date'].min(), end=daily_stats['date'].max())

daily_stats = daily_stats.set_index('date').reindex(date_range, fill_value=0).reset_index()

daily_stats.rename(columns={'index': 'date'}, inplace=True)

print(daily_stats)

output_file_path = 'daily_tweet_stats.csv'
daily_stats.to_csv(output_file_path, index=False)
print(f"Aggregated data with missing dates filled has been saved to {output_file_path}")
