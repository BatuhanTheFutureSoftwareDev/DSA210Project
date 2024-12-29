import json
import pandas as pd
from bs4 import BeautifulSoup  # Imported as per your request

# Function to extract JSON from HTML using BeautifulSoup (if needed)
def extract_json_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Assuming the JSON is within a <script> tag with type="application/json"
    script_tag = soup.find('script', type='application/json')
    if script_tag:
        return json.loads(script_tag.string)
    else:
        raise ValueError("No JSON script tag found in the HTML.")

# Replace 'my_tweets.json' with your JSON file path
json_file_path = 'my_tweets.json'

# If your JSON is embedded in an HTML file, use the extract_json_from_html function
# Otherwise, load the JSON directly
# Example for JSON file:
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# If extracting from HTML, uncomment and modify the following lines:
# with open('tweets.html', 'r', encoding='utf-8') as file:
#     html_content = file.read()
#     data = extract_json_from_html(html_content)

# List to store extracted tweet information
tweets_data = []

for entry in data:
    tweet = entry.get('tweet', {})
    
    # Extract creation date
    created_at_str = tweet.get('created_at', '')
    if not created_at_str:
        continue  # Skip if no creation date
    
    try:
        # Convert the created_at string to a pandas Timestamp
        created_at = pd.to_datetime(created_at_str)
        tweet_date = created_at.date()
    except Exception as e:
        print(f"Error parsing date '{created_at_str}': {e}")
        continue  # Skip if date parsing fails
    
    # Determine if the tweet is a retweet by checking if 'full_text' starts with 'RT @'
    full_text = tweet.get('full_text', '')
    is_retweet = 1 if full_text.startswith('RT @') else 0
    
    # Append the data to the list
    tweets_data.append({
        'date': tweet_date,
        'is_retweet': is_retweet
    })

# Create a DataFrame from the list
df = pd.DataFrame(tweets_data)

# Aggregate the number of tweets per day
tweet_counts = df.groupby('date').size().reset_index(name='tweet_count')

# Aggregate the number of retweets per day
retweet_counts = df.groupby('date')['is_retweet'].sum().reset_index(name='retweet_count')

# Merge the two DataFrames on the date
daily_stats = pd.merge(tweet_counts, retweet_counts, on='date')

# Sort the DataFrame by date
daily_stats = daily_stats.sort_values('date')

# Display the aggregated data
print(daily_stats)

# Save the aggregated data to a CSV file
output_file_path = 'daily_tweet_stats.csv'
daily_stats.to_csv(output_file_path, index=False)
print(f"Aggregated data has been saved to {output_file_path}")
