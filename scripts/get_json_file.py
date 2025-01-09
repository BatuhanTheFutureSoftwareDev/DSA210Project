import re
import json

input_file = "path/to/your/file/tweets.js"  # Replace with the path to your file
output_file = "my_tweets.json"

with open(input_file, "r") as file:
    js_data = file.read()

json_data = re.sub(r"window\.YTD\.tweets\.part0\s*=\s*", "", js_data).strip()

with open(output_file, "w") as file:
    file.write(json_data)

print(f"Extracted JSON saved to {output_file}")
