import requests
import pandas as pd

# Update this path to your cv-valid-dev folder
data_folder = 'cv-valid-dev'
csv_file = 'cv-valid-dev.csv'
api_url = 'http://localhost:8001/asr'

# # Load CSV
# df = pd.read_csv(csv_file)

# # Add empty column for generated text
# df['generated_text'] = ""

# for idx, row in tqdm(df.iterrows(), total=len(df)):
#     file_path = row['filename']

#     try:
#         with open(file_path, 'rb') as f:
#             files = {'file': f}
#             response = requests.post(api_url, files=files)
#             data = response.json()

#             df.at[idx, 'generated_text'] = data.get('transcription', '')
#             df.at[idx, 'duration'] = data.get('duration', '')

#     except Exception as e:
#         print(f"Failed on file {file_path}: {e}")

# # Save the updated CSV
# df.to_csv(csv_file, index=False)
# print("Transcriptions saved.")

import csv

updated_rows = []

with open(csv_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['generated_text']
    for i, row in enumerate(reader):
        if i >= 20:
            break
        file_path = row['filename']

        try:
            with open(file_path, 'rb') as f:
                response = requests.post(api_url, files={'file': f})
                data = response.json()
                row['generated_text'] = data.get('transcription', '')
                row['duration'] = data.get('duration', '')

        except Exception as e:
            print(f"Failed on file {file_path}: {e}")
            row['generated_text'] = ''
            row['duration'] = ''

        updated_rows.append(row)

with open(csv_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print("Transcriptions saved.")