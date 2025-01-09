import re
import json

# Step 1: Load the JavaScript file
input_file = "path/to/your/file/tweets.js"  # Replace with the path to your file
output_file = "my_tweets.json"

with open(input_file, "r") as file:
    js_data = file.read()

# Step 2: Remove the JavaScript wrapper
# Extract the JSON array using regex
json_data = re.sub(r"window\.YTD\.tweets\.part0\s*=\s*", "", js_data).strip()

# Step 3: Save as a JSON file
with open(output_file, "w") as file:
    file.write(json_data)

print(f"Extracted JSON saved to {output_file}")
