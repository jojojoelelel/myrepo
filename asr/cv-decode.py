import requests
import os
import csv
from tqdm import tqdm

input_folder = 'input'
output_folder = 'output'

input_csv_file = os.path.join(input_folder, 'cv-valid-dev.csv')
output_csv_file = os.path.join(output_folder, 'cv-valid-dev.csv')

api_url = 'http://localhost:8001/asr'

updated_rows = []

with open(input_csv_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['generated_text']
    for row in tqdm(reader):
        file_path = os.path.join(row['filename'])

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

with open(output_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print("Transcriptions saved.")