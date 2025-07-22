import json
import pandas as pd

# Load the JSON data
with open('extracted_properties.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Process each record
processed_data = []
for record in data:
    if isinstance(record, dict):  # Skip invalid entries
        if "error" in record:  # Skip error records
            continue
        processed_data.append(record)

# Normalize the JSON data
df = pd.json_normalize(processed_data)

# Save to CSV
df.to_csv('final_df.csv', index=False, encoding='utf-8')

print("CSV file created successfully: final_df.csv")