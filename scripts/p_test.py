import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('daily_tweet_stats.csv')
df['date'] = pd.to_datetime(df['date'])

target_date = pd.to_datetime('2023-02-06') # YYYY-MM-DD

# Set dynamic bounds
small_frame_lower = 0
small_frame_upper = 5
large_frame_lower = -20
large_frame_upper = 20

df['days_from_target'] = (df['date'] - target_date).dt.days

window_small = df[(df['days_from_target'] >= small_frame_lower) & 
                  (df['days_from_target'] <= small_frame_upper)]

window_large = df[(df['days_from_target'] >= large_frame_lower) & 
                  (df['days_from_target'] <= large_frame_upper) & 
                  (~df['days_from_target'].between(small_frame_lower, small_frame_upper))]

mean_small = window_small['tweet_count'].mean()
mean_large = window_large['tweet_count'].mean()
observed_diff = mean_small - mean_large

print(f"Mean (Small Window): {mean_small}")
print(f"Mean (Large Control Window excluding Small Window): {mean_large}")
print(f"Observed Difference: {observed_diff}")

# Permutation Test
n_permutations = 100000
diffs = []

combined_counts = np.concatenate([window_small['tweet_count'].values, window_large['tweet_count'].values])
labels = np.array([1]*len(window_small) + [0]*len(window_large))

for _ in range(n_permutations):
    np.random.shuffle(labels)
    group_small = combined_counts[labels == 1]
    group_large = combined_counts[labels == 0]
    diff = group_small.mean() - group_large.mean()
    diffs.append(diff)

# Calculate p-value
p_value = np.mean(np.abs(diffs) >= np.abs(observed_diff))
print(f"P-value: {p_value:.5f}")

# Visualization
plt.figure(figsize=(12, 6))
plt.hist(diffs, bins=50, alpha=0.7)
plt.axvline(observed_diff, color='red', linestyle='dashed', linewidth=2, label='Observed Diff')
plt.title('Permutation Test: Difference in Tweet Count (Dynamic Bounds)')
plt.xlabel('Difference in Means')
plt.ylabel('Frequency')
plt.legend()
plt.show()
