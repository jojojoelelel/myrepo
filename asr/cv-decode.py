import os
import requests
import pandas as pd
from tqdm import tqdm

# Update this path to your cv-valid-dev folder
data_folder = 'cv-valid-dev'
csv_file = 'cv-valid-dev.csv'
api_url = 'http://localhost:8001/asr'

# Load CSV
df = pd.read_csv(csv_file)

# Add empty column for generated text
df['generated_text'] = ""

for idx, row in tqdm(df.iterrows(), total=len(df)):
    file_path = row['filename']

    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(api_url, files=files)
            data = response.json()

            df.at[idx, 'generated_text'] = data.get('transcription', '')
            df.at[idx, 'duration'] = data.get('duration', '')

    except Exception as e:
        print(f"Failed on file {file_path}: {e}")

# Save the updated CSV
df.to_csv(csv_file, index=False)
print("Transcriptions saved.")
